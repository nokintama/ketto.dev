from django.contrib import admin
from .models import Match, MatchPlayer, Submission


class MatchPlayerInline(admin.TabularInline):
    model = MatchPlayer
    extra = 0
    fields = ('user', 'language', 'elo_before', 'elo_after', 'result')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem', 'status', 'mode', 'winner', 'created_at')
    list_filter = ('status', 'mode')
    search_fields = ('problem__title',)
    inlines = [MatchPlayerInline]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'match', 'user', 'verdict', 'tests_passed', 'runtime_ms', 'created_at')
    list_filter = ('verdict', 'language')
    search_fields = ('user__username',)