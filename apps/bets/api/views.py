from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction
from apps.wallets.models import Wallet, Transaction
from apps.bets.api.serializers import PlaceBetSerializer
from decimal import Decimal, ROUND_DOWN
from apps.bets.models import Bet, BetLine
from apps.riskengine.services import check_bet


class PlaceBetView(APIView):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        serializer = PlaceBetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lines = serializer.validated_data['lines']

        # calculate totals using Decimal to avoid precision issues
        total_stake_cents = 0
        potential_win_cents = 0
        for l in lines:
            stake_dec = Decimal(l['stake'])
            odds_dec = Decimal(l['odds'])
            stake_cents = int((stake_dec * 100).to_integral_value(rounding=ROUND_DOWN))
            total_stake_cents += stake_cents
            # potential win per line: stake * odds, rounded down to cents
            win_cents = int((stake_dec * odds_dec * 100).to_integral_value(rounding=ROUND_DOWN))
            potential_win_cents += win_cents

        # lock wallet row for update
        try:
            wallet = Wallet.objects.select_for_update().get(user=request.user)
        except Wallet.DoesNotExist:
            return Response({'detail': 'Wallet not found'}, status=status.HTTP_400_BAD_REQUEST)

        # risk checks
        risk = check_bet(request.user, total_stake_cents)
        if not risk.get('allowed'):
            return Response({'detail': 'risk_denied', 'reasons': risk.get('reasons')}, status=status.HTTP_400_BAD_REQUEST)

        available = wallet.balance_cents - wallet.reserved_balance_cents
        if available < total_stake_cents:
            return Response({'detail': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

        # reserve funds (mark as held)
        success = wallet.reserve(total_stake_cents)
        if not success:
            return Response({'detail': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

        # create hold transaction record
        Transaction.objects.create(wallet=wallet, amount_cents=-total_stake_cents, type='hold', status='completed')

        # create bet and lines
        bet = Bet.objects.create(user=request.user, total_stake_cents=total_stake_cents, potential_win_cents=potential_win_cents)
        for l in lines:
            BetLine.objects.create(
                bet=bet,
                event=l['event'],
                market=l['market'],
                selection=l['selection'],
                odds=l['odds'],
                stake_cents=int((Decimal(l['stake']) * 100).to_integral_value(rounding=ROUND_DOWN)),
            )

        return Response({'bet_id': bet.id, 'status': 'placed'}, status=status.HTTP_201_CREATED)


class QuoteBetView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PlaceBetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lines = serializer.validated_data['lines']

        total_stake_cents = 0
        potential_win_cents = 0
        for l in lines:
            stake_dec = Decimal(l['stake'])
            odds_dec = Decimal(l['odds'])
            stake_cents = int((stake_dec * 100).to_integral_value(rounding=ROUND_DOWN))
            total_stake_cents += stake_cents
            win_cents = int((stake_dec * odds_dec * 100).to_integral_value(rounding=ROUND_DOWN))
            potential_win_cents += win_cents

        # run risk check on quote too so UI can warn early
        risk = check_bet(request.user, total_stake_cents)

        return Response({
            'total_stake': f"{total_stake_cents/100:.2f}",
            'potential_win': f"{potential_win_cents/100:.2f}",
            'total_stake_cents': total_stake_cents,
            'potential_win_cents': potential_win_cents,
            'risk_allowed': risk.get('allowed'),
            'risk_reasons': risk.get('reasons'),
        })


class MyBetsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        bets = Bet.objects.filter(user=request.user).order_by('-placed_at')
        data = []
        for b in bets:
            data.append({
                'id': b.id,
                'status': b.status,
                'total_stake': f"{b.total_stake_cents/100:.2f}",
                'potential_win': f"{b.potential_win_cents/100:.2f}",
                'lines': [{'selection': ln.selection, 'odds': str(ln.odds), 'stake': f"{ln.stake_cents/100:.2f}"} for ln in b.lines.all()]
            })
        return Response(data)
