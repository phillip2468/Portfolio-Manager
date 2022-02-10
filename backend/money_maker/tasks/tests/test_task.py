from money_maker.tasks.task import update_yh_stocks


def test_get_stock_information(celery_session_worker):
    update_yh_stocks.delay()
