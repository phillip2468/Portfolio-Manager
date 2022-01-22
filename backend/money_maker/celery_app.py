from money_maker.app import init_celery
from money_maker.tasks.task import get_american_yh_stocks, update_asx_prices

app = init_celery()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60 * 15, update_asx_prices, name="update_asx_prices")
    sender.add_periodic_task(15, get_american_yh_stocks, name="get_american_stocks")
    