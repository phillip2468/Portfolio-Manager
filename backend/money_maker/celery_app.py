from money_maker.app import init_celery
from money_maker.tasks.task import update_asx_prices

app = init_celery()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    #sender.add_periodic_task(60 * 15, update_asx_prices, name="update_asx_prices")
    pass
