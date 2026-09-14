from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    display_name = models.CharField(max_length=50, blank=True)
    avatar_url = models.URLField(blank=True)
    bio = models.TextField(blank=True, max_length=500)
    elo = models.IntegerField(default=1000)
    peak_elo = models.IntegerField(default=1000)
    matches_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    preferred_language = models.CharField(max_length=20, default='python')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} ({self.elo})'


class UserProblemStats(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='problem_stats'
    )
    problem = models.ForeignKey(
        'problems.Problem',
        on_delete=models.CASCADE,
        related_name='user_stats'
    )
    attempts = models.IntegerField(default=0)
    solved = models.BooleanField(default=False)
    last_attempted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'problem')
        indexes = [
            models.Index(fields=['user', 'solved', 'last_attempted_at']),
        ]
        verbose_name = 'User statistics for the task'
        verbose_name_plural = 'User statistics by task'

    def __str__(self):
        return f'{self.user.username} — {self.problem.slug} (решил: {self.solved})'