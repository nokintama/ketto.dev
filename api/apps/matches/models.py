from django.db import models
from django.conf import settings


class Match(models.Model):
    class Status(models.TextChoices):
        WAITING = 'waiting', 'Waiting'
        IN_PROGRESS = 'in_progress', 'In_progress'
        FINISHED = 'finished', 'Finished'

    class Mode(models.TextChoices):
        RANKED = 'ranked', 'Ranked'
        TRAINING = 'training', 'Training'

    class EndReason(models.TextChoices):
        SOLVED = 'solved', 'Solved'
        TIMEOUT = 'timeout', 'Timeout'
        DISCONNECT = 'disconnect', 'Disconnect'
        SURRENDER = 'surrender', 'Surrender'

    problem = models.ForeignKey(
        'problems.Problem',
        on_delete=models.PROTECT,
        related_name='matches',
        verbose_name='Task'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.WAITING,
        verbose_name='Status'
    )
    mode = models.CharField(
        max_length=20,
        choices=Mode.choices,
        default=Mode.RANKED,
        verbose_name='Mode'
    )
    started_at = models.DateTimeField(null=True, blank=True, verbose_name='Начало')
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name='Конец')
    duration_ms = models.IntegerField(null=True, blank=True, verbose_name='Длительность (мс)')
    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='won_matches',
        verbose_name='Winner'
    )
    end_reason = models.CharField(
        max_length=20,
        choices=EndReason.choices,
        null=True, blank=True,
        verbose_name='Reason for completion'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = 'Match'
        verbose_name_plural = 'Matches'
        ordering = ['-created_at']

    def __str__(self):
        return f'Match #{self.id} ({self.get_status_display()})'


class MatchPlayer(models.Model):
    class Result(models.TextChoices):
        WIN = 'win', 'Win'
        LOSS = 'loss', 'Lose'
        DRAW = 'draw', 'Draw'

    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='players',
        verbose_name='Match'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='match_players',
        verbose_name='Player'
    )
    language = models.CharField(max_length=20, verbose_name='Language')
    elo_before = models.IntegerField(verbose_name='Elo Before')
    elo_after = models.IntegerField(null=True, blank=True, verbose_name='Elo after')
    elo_delta = models.IntegerField(null=True, blank=True, verbose_name='Rating changed')
    tests_passed = models.IntegerField(default=0, verbose_name='Tests passed')
    tests_total = models.IntegerField(default=0, verbose_name='All tests')
    solved_at = models.DateTimeField(null=True, blank=True, verbose_name='Solved at')
    result = models.CharField(
        max_length=20,
        choices=Result.choices,
        null=True, blank=True,
        verbose_name='Result'
    )

    class Meta:
        verbose_name = 'Player of match'
        verbose_name_plural = 'Players of match'
        unique_together = ('match', 'user')

    def __str__(self):
        return f'{self.user.username} in match #{self.match_id}'


class Submission(models.Model):
    class Verdict(models.TextChoices):
        ACCEPTED = 'accepted', 'Accepted'
        WRONG_ANSWER = 'wrong_answer', 'Wrong answer'
        TIME_LIMIT = 'time_limit', 'Time limit'
        MEMORY_LIMIT = 'memory_limit', 'Memory limit'
        RUNTIME_ERROR = 'runtime_error', 'Runtime error'
        COMPILATION_ERROR = 'compilation_error', 'Compilation error'

    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='Match'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='Player'
    )
    language = models.CharField(max_length=20, verbose_name='Language')
    code = models.TextField(verbose_name='Code')
    verdict = models.CharField(
        max_length=30,
        choices=Verdict.choices,
        verbose_name='Verdict'
    )
    tests_passed = models.IntegerField(default=0, verbose_name='Tests passed')
    tests_total = models.IntegerField(default=0, verbose_name='All tests')
    runtime_ms = models.IntegerField(null=True, blank=True, verbose_name='lead time (мс)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')

    class Meta:
        verbose_name = 'Submit'
        verbose_name_plural = 'Submits'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['match', 'user']),
        ]

    def __str__(self):
        return f'Submit #{self.id} ({self.get_verdict_display()})'