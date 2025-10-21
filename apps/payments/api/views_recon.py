from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from apps.payments.models_recon import (
	PaymentProvider, WithdrawalRequest, ReconciliationBatch, ReconciliationItem, ReconciliationReport
)
from apps.payments.api.serializers_recon import (
	PaymentProviderSerializer, WithdrawalRequestSerializer, ReconciliationBatchSerializer, ReconciliationItemSerializer, ReconciliationReportSerializer
)


class ReconciliationBatchViewSet(viewsets.ModelViewSet):
	queryset = ReconciliationBatch.objects.all().order_by('-created_at')
	serializer_class = ReconciliationBatchSerializer
	permission_classes = (IsAdminUser,)

	@action(detail=True, methods=['post'])
	def start_reconciliation(self, request, pk=None):
		batch = self.get_object()
		batch.status = 'processing'
		batch.save(update_fields=['status'])
		return Response({'status': 'processing'})

	@action(detail=True, methods=['get'])
	def summary(self, request, pk=None):
		batch = self.get_object()
		report, _ = ReconciliationReport.objects.get_or_create(batch=batch)
		return Response(ReconciliationReportSerializer(report).data)


class ReconciliationItemViewSet(viewsets.ModelViewSet):
	queryset = ReconciliationItem.objects.all().order_by('-created_at')
	serializer_class = ReconciliationItemSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		qs = super().get_queryset()
		batch = self.request.query_params.get('batch')
		status = self.request.query_params.get('status')
		if batch:
			qs = qs.filter(batch_id=batch)
		if status:
			qs = qs.filter(status=status)
		return qs


class PaymentProviderListView(generics.ListAPIView):
	queryset = PaymentProvider.objects.filter(active=True)
	serializer_class = PaymentProviderSerializer
	permission_classes = (AllowAny,)


class CreateWithdrawalRequestView(generics.CreateAPIView):
	serializer_class = WithdrawalRequestSerializer
	permission_classes = (IsAdminUser,)

	def create(self, request, *args, **kwargs):
		# tests create withdrawal as admin in a simple way; preserve default behaviour
		return super().create(request, *args, **kwargs)


class AdminWithdrawalActionView(generics.GenericAPIView):
	permission_classes = (IsAdminUser,)

	def post(self, request, pk, action):
		wr = get_object_or_404(WithdrawalRequest, pk=pk)
		if action == 'approve':
			wr.status = 'approved'
			wr.processed_at = None
			wr.save(update_fields=['status', 'processed_at'])
			return Response({'status': 'approved'})
		elif action == 'reject':
			wr.status = 'rejected'
			wr.save(update_fields=['status'])
			return Response({'status': 'rejected'})
		return Response({'detail': 'unknown action'}, status=status.HTTP_400_BAD_REQUEST)

