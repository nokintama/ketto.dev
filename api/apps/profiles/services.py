from apps.profiles.models import UserProblemStats
from django.utils import timezone

def update_problem_stats(user, problem, solved):
    stats, _ = UserProblemStats.objects.get_or_create(
        user=user,
        problem=problem,
    )
    stats.attempts += 1
    stats.solved = stats.solved or solved
    stats.last_attempted_at = timezone.now()
    stats.save()