from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.agents.models import Agent, AgentCommission
from apps.agents.api.serializers import AgentSerializer, AgentCommissionSerializer
from apps.wallets.models import Transaction
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import csv
from datetime import datetime
from rest_framework.pagination import PageNumberPagination
from apps.agents.api.serializers import TransactionSerializer


class MyAgentProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            agent = Agent.objects.get(user=request.user)
        except Agent.DoesNotExist:
            return Response({'detail': 'Not an agent'}, status=404)
        return Response(AgentSerializer(agent).data)


class AgentCommissions(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            agent = Agent.objects.get(user=request.user)
        except Agent.DoesNotExist:
            return Response({'detail': 'Not an agent'}, status=404)
        qs = AgentCommission.objects.filter(agent=agent)
        return Response(AgentCommissionSerializer(qs, many=True).data)


class CommissionReportView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # optional date range: ?from=YYYY-MM-DD&to=YYYY-MM-DD
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')

        txs = Transaction.objects.filter(type='commission', status='completed')
        if from_date:
            try:
                fd = datetime.fromisoformat(from_date)
                txs = txs.filter(created_at__gte=fd)
            except Exception:
                return Response({'detail': 'invalid from date'}, status=status.HTTP_400_BAD_REQUEST)
        if to_date:
            try:
                td = datetime.fromisoformat(to_date)
                txs = txs.filter(created_at__lte=td)
            except Exception:
                return Response({'detail': 'invalid to date'}, status=status.HTTP_400_BAD_REQUEST)

        # If user is staff, return report for all agents; otherwise only for their agent profile
        if request.user.is_staff:
            group = txs.values('wallet__user__agent__id', 'wallet__user__agent__name')\
                       .annotate(total_cents=Sum('amount_cents'))
        else:
            try:
                agent = Agent.objects.get(user=request.user)
            except Agent.DoesNotExist:
                return Response({'detail': 'Not an agent'}, status=status.HTTP_403_FORBIDDEN)
            group = txs.filter(wallet__user__agent=agent)\
                       .values('wallet__user__agent__id', 'wallet__user__agent__name')\
                       .annotate(total_cents=Sum('amount_cents'))

        data = []
        for item in group:
            data.append({
                'agent_id': item.get('wallet__user__agent__id'),
                'agent_name': item.get('wallet__user__agent__name'),
                'total_cents': item.get('total_cents') or 0,
                'total_amount': f"{((item.get('total_cents') or 0)/100):.2f}",
            })
        return Response(data)


class CommissionExportCSV(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if not request.user.is_staff:
            return Response({'detail': 'staff only'}, status=status.HTTP_403_FORBIDDEN)

        # reuse report logic
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        txs = Transaction.objects.filter(type='commission', status='completed')
        if from_date:
            try:
                fd = datetime.fromisoformat(from_date)
                txs = txs.filter(created_at__gte=fd)
            except Exception:
                return Response({'detail': 'invalid from date'}, status=status.HTTP_400_BAD_REQUEST)
        if to_date:
            try:
                td = datetime.fromisoformat(to_date)
                txs = txs.filter(created_at__lte=td)
            except Exception:
                return Response({'detail': 'invalid to date'}, status=status.HTTP_400_BAD_REQUEST)

        group = txs.values('wallet__user__agent__id', 'wallet__user__agent__name')\
                   .annotate(total_cents=Sum('amount_cents'))

        # build CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="agent_commissions.csv"'
        writer = csv.writer(response)
        writer.writerow(['agent_id', 'agent_name', 'total_amount'])
        for item in group:
            total = (item.get('total_cents') or 0)/100
            writer.writerow([item.get('wallet__user__agent__id'), item.get('wallet__user__agent__name'), f"{total:.2f}"])
        return response


class CommissionDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        qs = Transaction.objects.filter(type='commission', status='completed').order_by('-created_at')
        if from_date:
            try:
                fd = datetime.fromisoformat(from_date)
                qs = qs.filter(created_at__gte=fd)
            except Exception:
                return Response({'detail': 'invalid from date'}, status=status.HTTP_400_BAD_REQUEST)
        if to_date:
            try:
                td = datetime.fromisoformat(to_date)
                qs = qs.filter(created_at__lte=td)
            except Exception:
                return Response({'detail': 'invalid to date'}, status=status.HTTP_400_BAD_REQUEST)

        # Non-staff users only see their agent's commission transactions
        if not request.user.is_staff:
            try:
                agent = Agent.objects.get(user=request.user)
            except Agent.DoesNotExist:
                return Response({'detail': 'Not an agent'}, status=status.HTTP_403_FORBIDDEN)
            # Filter commission transactions belonging to this agent's own wallet
            qs = qs.filter(wallet__user=agent.user)

        paginator = PageNumberPagination()
        paginator.page_size = int(request.query_params.get('page_size', 25))
        page = paginator.paginate_queryset(qs, request)
        serializer = TransactionSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
