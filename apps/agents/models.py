from django.db import models
from django.conf import settings


class Agent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agent_profile')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='downline')
    name = models.CharField(max_length=128)
    approved = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Agent({self.name}) [{self.user.email}]"


class AgentCommission(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='commissions')
    percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text='Commission percentage (e.g., 3.50)')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commission({self.agent.name}) {self.percentage}%"


class AgentPayout(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='payouts')
    amount_cents = models.BigIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"AgentPayout({self.agent.name}) {self.amount_cents} {self.status}"
