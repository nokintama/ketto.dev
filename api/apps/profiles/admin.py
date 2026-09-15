from django.contrib import admin
from .models import Profile, Badge, UserBadge, UserProblemStats


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


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'color', 'is_assignable')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_assignable',)
    search_fields = ('slug', 'name')


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'assigned_at')
    list_filter = ('badge',)
    search_fields = ('user__username',)