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