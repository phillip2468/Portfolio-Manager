from unittest.mock import patch

import pytest
from money_maker.tasks.task import update_yh_stocks


def test_get_stock_information():
    task_handle = update_yh_stocks.delay()
    task_handle.get()
