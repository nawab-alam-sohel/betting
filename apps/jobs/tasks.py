from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def backup_task():
    """Placeholder daily backup task."""
    logger.info("[jobs] backup_task started")
    # TODO: implement DB dump or use cloud backup service
    logger.info("[jobs] backup_task finished")
