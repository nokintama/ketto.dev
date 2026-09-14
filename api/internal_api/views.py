from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.problems.models import Problem
from apps.matches.models import Match, MatchPlayer, Submission
from apps.profiles.models import Profile
from apps.profiles.services import update_problem_stats
from apps.rating.services import calculate_elo
from apps.accounts.models import User
from .auth import HasServiceToken


# ========== PROBLEMS ==========

class PickProblemView(APIView):
    permission_classes = [HasServiceToken]

    def get(self, request):
        difficulty = request.query_params.get('difficulty')
        exclude = request.query_params.getlist('exclude')

        qs = Problem.objects.filter(is_public=True)
        if difficulty:
            qs = qs.filter(difficulty=difficulty)
        if exclude:
            qs = qs.exclude(id__in=exclude)

        problem = qs.order_by('?').first()
        if not problem:
            return Response({'error': 'no problems'}, status=404)

        return Response({
            'id': problem.id,
            'slug': problem.slug,
            'title': problem.title,
            'statement_md': problem.statement_md,
            'difficulty': problem.difficulty,
            'time_limit_ms': problem.time_limit_ms,
            'memory_limit_mb': problem.memory_limit_mb,
        })


class ProblemTestsView(APIView):
    permission_classes = [HasServiceToken]

    def get(self, request, problem_id):
        problem = get_object_or_404(Problem, id=problem_id)
        include_hidden = request.query_params.get('hidden') == 'true'

        tests = problem.test_cases.all()
        if not include_hidden:
            tests = tests.filter(is_public=True)

        return Response({
            'problem_id': problem.id,
            'tests': [
                {
                    'id': t.id,
                    'input': t.input,
                    'expected': t.expected,
                    'is_public': t.is_public,
                    'order': t.order,
                }
                for t in tests
            ]
        })


# ========== MATCHES ==========

class CreateMatchView(APIView):
    permission_classes = [HasServiceToken]

    @transaction.atomic
    def post(self, request):
        problem_id = request.data.get('problem_id')
        mode = request.data.get('mode', 'ranked')
        players = request.data.get('players') # [{"user_id": 1, "language": "python"}, ...]

        if not problem_id:
            return Response(
                {'error': 'problem_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not players or not isinstance(players, list):
            return Response(
                {'error': 'players must be a non-empty list'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if len(players) != 2:
            return Response(
                {'error': 'exactly 2 players required'},
                status=status.HTTP_400_BAD_REQUEST
        )

        problem = get_object_or_404(Problem, id=problem_id)

        match = Match.objects.create(
            problem=problem,
            status=Match.Status.IN_PROGRESS,
            mode=mode,
            started_at=timezone.now(),
        )

        result_players = []
        for p in players:
            user = get_object_or_404(User, id=p['user_id'])
            profile = user.profile

            mp = MatchPlayer.objects.create(
                match=match,
                user=user,
                language=p['language'],
                elo_before=profile.elo,
            )
            result_players.append({
                'user_id': user.id,
                'username': user.username,
                'elo_before': profile.elo,
                'language': p['language'],
            })

        return Response({
            'id': match.id,
            'problem_id': problem.id,
            'status': match.status,
            'players': result_players,
        }, status=status.HTTP_201_CREATED)


class FinishMatchView(APIView):
    permission_classes = [HasServiceToken]

    @transaction.atomic
    def post(self, request, match_id):
        match = Match.objects.select_for_update().get(id=match_id)

        # Идемпотентность
        if match.status == Match.Status.FINISHED:
            return Response({
                'status': 'already_finished',
                'winner_id': match.winner_id,
            })

        winner_id = request.data.get('winner_id')
        loser_id = request.data.get('loser_id')
        end_reason = request.data.get('end_reason', Match.EndReason.SOLVED)

        winner_player = match.players.get(user_id=winner_id)
        loser_player = match.players.get(user_id=loser_id)

        winner_profile = winner_player.user.profile
        loser_profile = loser_player.user.profile

        # Эло
        new_winner_elo, new_loser_elo = calculate_elo(
            winner_player.elo_before,
            loser_player.elo_before,
            winner_profile.matches_played,
            loser_profile.matches_played,
        )

        # Обновляем MatchPlayer
        winner_player.elo_after = new_winner_elo
        winner_player.elo_delta = new_winner_elo - winner_player.elo_before
        winner_player.result = MatchPlayer.Result.WIN
        winner_player.solved_at = timezone.now()
        winner_player.save()

        loser_player.elo_after = new_loser_elo
        loser_player.elo_delta = new_loser_elo - loser_player.elo_before
        loser_player.result = MatchPlayer.Result.LOSS
        loser_player.save()

        # Обновляем профили
        winner_profile.elo = new_winner_elo
        winner_profile.peak_elo = max(winner_profile.peak_elo, new_winner_elo)
        winner_profile.matches_played += 1
        winner_profile.wins += 1
        winner_profile.save()

        loser_profile.elo = new_loser_elo
        loser_profile.matches_played += 1
        loser_profile.losses += 1
        loser_profile.save()

        # Статистика по задаче
        update_problem_stats(winner_player.user, match.problem, solved=True)
        update_problem_stats(loser_player.user, match.problem, solved=False)

        # Завершаем матч
        match.status = Match.Status.FINISHED
        match.winner_id = winner_id
        match.end_reason = end_reason
        match.finished_at = timezone.now()
        if match.started_at:
            match.duration_ms = int((match.finished_at - match.started_at).total_seconds() * 1000)
        match.save()

        return Response({
            'status': 'ok',
            'winner_id': winner_id,
            'winner_elo': new_winner_elo,
            'loser_elo': new_loser_elo,
            'winner_delta': winner_player.elo_delta,
            'loser_delta': loser_player.elo_delta,
        })


# ========== SUBMISSIONS ==========

class CreateSubmissionView(APIView):
    permission_classes = [HasServiceToken]

    def post(self, request):
        match_id = request.data.get('match_id')
        user_id = request.data.get('user_id')

        match = get_object_or_404(Match, id=match_id)
        user = get_object_or_404(User, id=user_id)

        submission = Submission.objects.create(
            match=match,
            user=user,
            language=request.data.get('language'),
            code=request.data.get('code'),
            verdict=request.data.get('verdict'),
            tests_passed=request.data.get('tests_passed', 0),
            tests_total=request.data.get('tests_total', 0),
            runtime_ms=request.data.get('runtime_ms'),
        )

        return Response({
            'id': submission.id,
            'status': 'created',
        }, status=status.HTTP_201_CREATED)


# ========== USERS ==========

class UserRatingView(APIView):
    permission_classes = [HasServiceToken]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        profile = user.profile

        return Response({
            'user_id': user.id,
            'username': user.username,
            'elo': profile.elo,
            'peak_elo': profile.peak_elo,
            'matches_played': profile.matches_played,
            'wins': profile.wins,
            'losses': profile.losses,
            'preferred_language': profile.preferred_language,
        })