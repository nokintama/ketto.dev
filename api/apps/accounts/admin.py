from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.profiles.models import UserBadge
from .models import User


class UserBadgeInline(admin.TabularInline):
    model = UserBadge
    extra = 0
    fields = ('badge', 'assigned_at')
    readonly_fields = ('assigned_at',)
    autocomplete_fields = ('badge',)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Ban', {'fields': ('is_banned', 'ban_reason')}),
    )
    list_display = ('username', 'email', 'is_banned', 'date_joined')
    list_filter = ('is_banned',)
    inlines = [UserBadgeInline]