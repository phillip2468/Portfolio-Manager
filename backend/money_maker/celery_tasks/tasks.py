from celery import shared_task


@shared_task(name='celery_tasks.add_together')
def add_together():
    return 10 + 10
