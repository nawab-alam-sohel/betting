from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from apps.users.models import User
from apps.wallets.models import Transaction
from apps.bets.models import Bet
from apps.payments.models import PaymentIntent
from apps.payments.models_recon import WithdrawalRequest
from apps.users.models_kyc import KYCDocument, LoginAttempt, UserDevice
from apps.sports.models import Game
from apps.sports.models import SportsProvider
from apps.casino.models import CasinoProvider
from rest_framework import status


class DashboardSummaryView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        now = timezone.now()
        last_30 = now - timedelta(days=30)

        total_bettors = User.objects.count()
        active_bettors = User.objects.filter(is_active=True, is_banned=False).count()
        email_unverified = User.objects.filter(email_verified=False).count()
        mobile_unverified = User.objects.filter(phone_verified=False).count()

        # Games (based on apps.sports.models.Game)
        in_play_games = Game.objects.filter(status='live').count()
        upcoming_games = Game.objects.filter(status='scheduled', start_time__gte=now).count()
        open_for_betting = Game.objects.filter(status__in=['scheduled']).count()
        not_open_for_betting = Game.objects.filter(status__in=['closed']).count()

        deposits_total_cents = (
            Transaction.objects.filter(type='deposit', status='completed')
            .aggregate(s=Sum('amount_cents'))['s'] or 0
        )
        pending_deposits = PaymentIntent.objects.filter(status='pending').count()
        rejected_deposits = PaymentIntent.objects.filter(status='failed').count()
        deposit_charge_cents = 0  # not modeled; keep 0

        withdrawals_total_cents = (
            Transaction.objects.filter(type='withdraw', status='completed')
            .aggregate(s=Sum('amount_cents'))['s'] or 0
        )
        pending_withdrawals = WithdrawalRequest.objects.filter(status='pending').count()
        rejected_withdrawals = WithdrawalRequest.objects.filter(status='rejected').count()
        withdrawal_charge_cents = 0

        pending_bets = Bet.objects.filter(status='placed').count()
        won_bets = Bet.objects.filter(result='won').count()
        lost_bets = Bet.objects.filter(result='lost').count()
        refunded_bets = Bet.objects.filter(result='refunded').count()
        pending_support_tickets = 0  # no ticketing app yet

        pending_kyc = KYCDocument.objects.filter(status='pending').count()
        pending_outcomes = 0  # requires sports settlement flow

        data = {
            'users': {
                'total_bettors': total_bettors,
                'active_bettors': active_bettors,
                'email_unverified': email_unverified,
                'mobile_unverified': mobile_unverified,
            },
            'games': {
                'in_play': in_play_games,
                'upcoming': upcoming_games,
                'open_for_betting': open_for_betting,
                'not_open_for_betting': not_open_for_betting,
                'closed': Game.objects.filter(status='closed').count(),
                'ended': Game.objects.filter(status='ended').count(),
                'cancelled': Game.objects.filter(status='cancelled').count(),
            },
            'deposits': {
                'total_cents': deposits_total_cents,
                'pending': pending_deposits,
                'rejected': rejected_deposits,
                'charge_cents': deposit_charge_cents,
            },
            'withdrawals': {
                'total_cents': withdrawals_total_cents,
                'pending': pending_withdrawals,
                'rejected': rejected_withdrawals,
                'charge_cents': withdrawal_charge_cents,
            },
            'bets': {
                'pending': pending_bets,
                'won': won_bets,
                'lost': lost_bets,
                'refunded': refunded_bets,
            },
            'support': {
                'pending_tickets': pending_support_tickets,
            },
            'kyc': {
                'pending': pending_kyc,
            },
            'outcomes': {
                'pending': pending_outcomes,
            },
            'time_window_days': 30,
        }
        return Response(data)


class DashboardChartsView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        now = timezone.now()
        start = now - timedelta(days=30)

        # Aggregate deposits vs withdraws per day
        deposits = (
            Transaction.objects.filter(type='deposit', status='completed', created_at__gte=start)
            .extra(select={'day': "date(created_at)"})
            .values('day')
            .annotate(total_cents=Sum('amount_cents'))
            .order_by('day')
        )
        withdraws = (
            Transaction.objects.filter(type='withdraw', status='completed', created_at__gte=start)
            .extra(select={'day': "date(created_at)"})
            .values('day')
            .annotate(total_cents=Sum('amount_cents'))
            .order_by('day')
        )

        # Transactions report: plus vs minus per day
        plus_tx = (
            Transaction.objects.filter(type__in=['deposit','win','commission'], status='completed', created_at__gte=start)
            .extra(select={'day': "date(created_at)"})
            .values('day')
            .annotate(total_cents=Sum('amount_cents'))
            .order_by('day')
        )
        minus_tx = (
            Transaction.objects.filter(type__in=['withdraw','bet','hold'], status='completed', created_at__gte=start)
            .extra(select={'day': "date(created_at)"})
            .values('day')
            .annotate(total_cents=Sum('amount_cents'))
            .order_by('day')
        )

        # Login analytics (last 30 days)
        # LoginAttempt model doesn't store browser/os_type; use UserDevice as source for those.
        device_qs = UserDevice.objects.filter(last_used__gte=start)
        by_browser = list(device_qs.values('browser').annotate(count=Count('id')).order_by('-count')[:10])
        by_os = list(device_qs.values('os_type').annotate(count=Count('id')).order_by('-count')[:10])
        # Country/location can come from LoginAttempt, fall back to UserDevice if needed
        login_qs = LoginAttempt.objects.filter(attempted_at__gte=start)
        by_country = list(login_qs.values('location').annotate(count=Count('id')).order_by('-count')[:10])
        if not by_country:
            by_country = list(device_qs.values('location').annotate(count=Count('id')).order_by('-count')[:10])

        data = {
            'deposits_daily': list(deposits),
            'withdraws_daily': list(withdraws),
            'transactions_plus_daily': list(plus_tx),
            'transactions_minus_daily': list(minus_tx),
            'login_by_browser': by_browser,
            'login_by_os': by_os,
            'login_by_country': by_country,
        }
        return Response(data)


class AdminSportsProviderView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        p = SportsProvider.objects.order_by('-updated_at').first()
        if not p:
            return Response({
                'key': 'default', 'name': 'Sports Provider', 'base_url': '',
                'config': {'api_key': ''}, 'active': False,
            })
        return Response({
            'key': p.key, 'name': p.name, 'base_url': p.base_url,
            'config': p.config, 'active': p.active,
        })

    def put(self, request):
        payload = request.data or {}
        key = payload.get('key') or 'default'
        p, _ = SportsProvider.objects.get_or_create(key=key, defaults={'name': payload.get('name') or key.title()})
        p.name = payload.get('name') or p.name
        p.base_url = payload.get('base_url') or ''
        cfg = p.config or {}
        api_key = (payload.get('config') or {}).get('api_key')
        if api_key is not None:
            cfg['api_key'] = api_key
        # pass-through any other config keys
        for k, v in (payload.get('config') or {}).items():
            if k != 'api_key':
                cfg[k] = v
        p.config = cfg
        if 'active' in payload:
            p.active = bool(payload['active'])
        p.save()
        return Response({'ok': True}, status=status.HTTP_200_OK)


class AdminCasinoProviderView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        p = CasinoProvider.objects.order_by('display_order', 'name').first()
        if not p:
            return Response({
                'key': 'generic', 'name': 'Casino Provider', 'base_url': '',
                'config': {'api_key': ''}, 'active': False,
            })
        return Response({
            'key': p.key, 'name': p.name, 'base_url': p.base_url,
            'config': p.config, 'active': p.active,
        })

    def put(self, request):
        payload = request.data or {}
        key = payload.get('key') or 'generic'
        p, _ = CasinoProvider.objects.get_or_create(key=key, defaults={'name': payload.get('name') or key.title()})
        p.name = payload.get('name') or p.name
        p.base_url = payload.get('base_url') or ''
        cfg = p.config or {}
        api_key = (payload.get('config') or {}).get('api_key')
        if api_key is not None:
            cfg['api_key'] = api_key
        for k, v in (payload.get('config') or {}).items():
            if k != 'api_key':
                cfg[k] = v
        p.config = cfg
        if 'active' in payload:
            p.active = bool(payload['active'])
        p.save()
        return Response({'ok': True}, status=status.HTTP_200_OK)


class AdminDepositsSummaryView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        return Response({
            'pending': PaymentIntent.objects.filter(status='pending').count(),
            'successful': PaymentIntent.objects.filter(status='completed').count(),
            'rejected': PaymentIntent.objects.filter(status='failed').count(),
            'initiated': PaymentIntent.objects.filter(status='initiated').count(),
            'approved': PaymentIntent.objects.filter(status='completed').count(),  # map approved≈completed
            'all': PaymentIntent.objects.all().count(),
        })


class AdminDepositsListView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        status_param = request.query_params.get('status')
        page = int(request.query_params.get('page', '1'))
        page_size = min(int(request.query_params.get('page_size', '25')), 200)

        qs = PaymentIntent.objects.select_related('user').order_by('-created_at')
        if status_param and status_param != 'all':
            # map UI synonyms
            if status_param in ['approved', 'successful']:
                qs = qs.filter(status='completed')
            elif status_param in ['rejected']:
                qs = qs.filter(status='failed')
            else:
                qs = qs.filter(status=status_param)

        total = qs.count()
        start = (page - 1) * page_size
        items = [
            {
                'id': pi.id,
                'user': getattr(pi.user, 'email', None) or getattr(pi.user, 'username', None),
                'provider': pi.provider,
                'amount_cents': pi.amount_cents,
                'currency': pi.currency,
                'status': pi.status,
                'created_at': pi.created_at,
                'reference': pi.reference,
            }
            for pi in qs[start:start + page_size]
        ]
        return Response({'count': total, 'page': page, 'page_size': page_size, 'results': items})


class AdminWithdrawalsSummaryView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        return Response({
            'pending': WithdrawalRequest.objects.filter(status='pending').count(),
            'approved': WithdrawalRequest.objects.filter(status='approved').count(),
            'rejected': WithdrawalRequest.objects.filter(status='rejected').count(),
            'all': WithdrawalRequest.objects.all().count(),
        })


class AdminWithdrawalsListView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        status_param = request.query_params.get('status')
        page = int(request.query_params.get('page', '1'))
        page_size = min(int(request.query_params.get('page_size', '25')), 200)

        qs = WithdrawalRequest.objects.select_related('user', 'provider').order_by('-created_at')
        if status_param and status_param != 'all':
            qs = qs.filter(status=status_param)

        total = qs.count()
        start = (page - 1) * page_size
        items = [
            {
                'id': wr.id,
                'user': getattr(wr.user, 'email', None) or getattr(wr.user, 'username', None),
                'amount_cents': wr.amount_cents,
                'provider': wr.provider.name if wr.provider_id else None,
                'status': wr.status,
                'created_at': wr.created_at,
                'processed_at': wr.processed_at,
                'reference': wr.reference,
            }
            for wr in qs[start:start + page_size]
        ]
        return Response({'count': total, 'page': page, 'page_size': page_size, 'results': items})
