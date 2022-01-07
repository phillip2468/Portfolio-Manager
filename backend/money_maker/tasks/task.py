from __future__ import absolute_import, unicode_literals

import dramatiq


@dramatiq.actor
def add_together():
    return 10 + 10000000000

