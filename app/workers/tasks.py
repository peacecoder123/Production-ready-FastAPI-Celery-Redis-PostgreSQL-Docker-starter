from __future__ import annotations

import logging
import time
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="process_item")
def process_item(item_id: int, payload: dict | None = None) -> dict:
    """Example background task to process an item."""
    logger.info("Processing item %s with payload %s", item_id, payload)
    time.sleep(1)  # Simulate some heavy compute or external API call
    return {
        "status": "completed",
        "item_id": item_id,
        "processed_at": time.time(),
    }


@celery_app.task(name="send_notification")
def send_notification(recipient: str, message: str) -> dict:
    """Example background task to send an alert or notification."""
    logger.info("Sending notification to %s: %s", recipient, message)
    return {
        "status": "sent",
        "recipient": recipient,
        "length": len(message),
    }
