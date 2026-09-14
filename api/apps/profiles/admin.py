from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'elo', 'matches_played', 'wins', 'losses')
    search_fields = ('user__username',)
    list_filter = ('preferred_language',)