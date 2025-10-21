from rest_framework import serializers
from apps.bets.models import Bet, BetLine


from decimal import Decimal


class BetLineSerializer(serializers.ModelSerializer):
    stake = serializers.DecimalField(max_digits=12, decimal_places=2)
    odds = serializers.DecimalField(max_digits=9, decimal_places=4)

    class Meta:
        model = BetLine
        fields = ('event', 'market', 'selection', 'odds', 'stake',)


class PlaceBetSerializer(serializers.Serializer):
    lines = BetLineSerializer(many=True)

    def validate(self, data):
        if not data.get('lines'):
            raise serializers.ValidationError('At least one bet line is required')
        return data
