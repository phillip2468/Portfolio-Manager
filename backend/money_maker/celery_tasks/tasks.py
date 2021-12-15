from celery import shared_task


@shared_task
def add_together():
    return 10 + 10
