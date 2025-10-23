from rest_framework import serializers
from apps.casino.models import CasinoProvider, CasinoCategory, CasinoGame, CasinoSession


class CasinoProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CasinoProvider
        fields = ("id", "key", "name")


class CasinoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CasinoCategory
        fields = ("id", "name", "slug")


class CasinoGameSerializer(serializers.ModelSerializer):
    provider = CasinoProviderSerializer(read_only=True)
    categories = CasinoCategorySerializer(many=True, read_only=True)

    class Meta:
        model = CasinoGame
        fields = (
            "id",
            "name",
            "slug",
            "thumbnail_url",
            "rtp",
            "volatility",
            "active",
            "provider",
            "categories",
        )


class LaunchGameSerializer(serializers.Serializer):
    game_id = serializers.IntegerField()
