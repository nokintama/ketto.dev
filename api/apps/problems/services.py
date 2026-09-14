from django.utils import timezone
from datetime import timedelta
from apps.profiles.models import UserProblemStats
from .models import Problem


def pick_problem_for_user(user, difficulty=None):
    recent_threshold = timezone.now() - timedelta(days=7)
    recent_problems = UserProblemStats.objects.filter(
        user=user,
        last_attempted_at__gte=recent_threshold,
    ).values_list('problem_id', flat=True)

    base_qs = Problem.objects.filter(is_public=True)
    if difficulty:
        base_qs = base_qs.filter(difficulty=difficulty)

    tried = UserProblemStats.objects.filter(user=user).values_list('problem_id', flat=True)
    never_tried = base_qs.exclude(id__in=tried)

    if never_tried.exists():
        return never_tried.order_by('?').first()

    long_ago = base_qs.exclude(id__in=recent_problems)

    if long_ago.exists():
        return long_ago.order_by('?').first()

    return base_qs.order_by('?').first()