from money_maker.app import create_app
from money_maker.tasks.task import update_yh_stocks

app = create_app()


@app.route("/")
def index():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run()
