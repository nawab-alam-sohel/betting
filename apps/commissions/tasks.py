from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def generate_agent_commissions_task():
    """
    Placeholder: compute and create agent commission entries for the previous day.
    TODO: implement actual commission rules and aggregation logic.
    """
    logger.info("[commissions] generate_agent_commissions_task started")
    # Implement aggregation across bets/turnover and write AgentCommission/ledger rows
    logger.info("[commissions] generate_agent_commissions_task finished")
