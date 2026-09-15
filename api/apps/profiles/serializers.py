from rest_framework import serializers
from .models import Badge, Profile, UserBadge, UserProblemStats


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ('slug', 'name', 'description', 'color', 'icon')


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    badges = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'id', 'username', 'display_name', 'avatar_url', 'bio',
            'elo', 'peak_elo', 'matches_played', 'wins', 'losses',
            'preferred_language', 'badges', 'updated_at'
        )
        read_only_fields = ('elo', 'peak_elo', 'matches_played', 'wins', 'losses')

    def get_badges(self, obj):
        user_badges = obj.user.badges.select_related('badge').all()
        return BadgeSerializer([ub.badge for ub in user_badges], many=True).data