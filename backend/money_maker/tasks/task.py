from __future__ import absolute_import, unicode_literals

from celery import shared_task


@shared_task
def add_together():
    return 10 + 10000000000

