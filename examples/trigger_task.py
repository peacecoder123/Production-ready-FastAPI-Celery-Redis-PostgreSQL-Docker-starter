#!/usr/bin/env python3
"""
Example showing how to queue a Celery task asynchronously from Python.
"""

from app.workers.tasks import process_item, send_notification


def main():
    print("Dispatching asynchronous background task 'process_item'...")
    task = process_item.delay(42, {"source": "cli_trigger", "priority": "high"})
    print(f"Task dispatched with ID: {task.id}")
    print("Status:", task.status)

    print("\nDispatching asynchronous 'send_notification'...")
    n_task = send_notification.delay("dev@example.com", "Pipeline processing finished.")
    print(f"Notification task dispatched with ID: {n_task.id}")


if __name__ == "__main__":
    main()
