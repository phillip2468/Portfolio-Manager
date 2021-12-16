from money_maker.app import init_celery

app = init_celery()
app.conf.imports = app.conf.imports + ("money_maker.tasks.task",)
