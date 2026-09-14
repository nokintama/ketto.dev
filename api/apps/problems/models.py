from django.db import models
from django.conf import settings


class Problem(models.Model):
    class Difficulty(models.TextChoices):
        EASY = 'easy', 'Easy'
        MEDIUM = 'medium', 'Medium'
        HARD = 'hard', 'Hard'

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    statement_md = models.TextField()
    difficulty = models.CharField(max_length=20, choices=Difficulty.choices)
    topics = models.JSONField(default=list, blank=True)
    time_limit_ms = models.IntegerField(default=2000)
    memory_limit_mb = models.IntegerField(default=256)
    is_public = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_problems'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.difficulty})'


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input = models.JSONField()
    expected = models.JSONField()
    is_public = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.problem.title} — test #{self.order}'