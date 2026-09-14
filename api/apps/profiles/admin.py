from django.contrib import admin
from .models import Profile, UserProblemStats


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'elo', 'matches_played', 'wins', 'losses')
    search_fields = ('user__username',)
    list_filter = ('preferred_language',)


@admin.register(UserProblemStats)
class UserProblemStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'attempts', 'solved', 'last_attempted_at')
    list_filter = ('solved',)
    search_fields = ('user__username', 'problem__title')