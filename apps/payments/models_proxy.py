from .models import PaymentIntent
from .models_recon import WithdrawalRequest

# PaymentIntent proxies for deposit statuses
class PaymentIntentPending(PaymentIntent):
    class Meta:
        proxy = True
        verbose_name = "Pending Deposit"
        verbose_name_plural = "Pending Deposits"

class PaymentIntentCompleted(PaymentIntent):
    class Meta:
        proxy = True
        verbose_name = "Completed Deposit"
        verbose_name_plural = "Completed Deposits"

class PaymentIntentFailed(PaymentIntent):
    class Meta:
        proxy = True
        verbose_name = "Failed Deposit"
        verbose_name_plural = "Failed Deposits"

# WithdrawalRequest proxies for withdrawal statuses
class WithdrawalRequestPending(WithdrawalRequest):
    class Meta:
        proxy = True
        verbose_name = "Pending Withdrawal"
        verbose_name_plural = "Pending Withdrawals"

class WithdrawalRequestApproved(WithdrawalRequest):
    class Meta:
        proxy = True
        verbose_name = "Approved Withdrawal"
        verbose_name_plural = "Approved Withdrawals"

class WithdrawalRequestRejected(WithdrawalRequest):
    class Meta:
        proxy = True
        verbose_name = "Rejected Withdrawal"
        verbose_name_plural = "Rejected Withdrawals"
