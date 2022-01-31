from money_maker.app import init_celery
from money_maker.tasks.task import update_yh_stocks

app = init_celery()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30, update_yh_stocks, name="update_yh_stocks")
