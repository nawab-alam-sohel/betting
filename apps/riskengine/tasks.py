from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def risk_monitor_task():
    """Placeholder hourly risk monitoring task."""
    logger.info("[riskengine] risk_monitor_task running")
    # TODO: scan for abnormal bet patterns, suspicious velocity, etc.
    logger.info("[riskengine] risk_monitor_task done")
