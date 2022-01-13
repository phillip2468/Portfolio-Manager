import os

from money_maker.app import create_app

app = create_app()


@app.route('/', defaults={'path': ''})  # homepage
@app.route('/<path:path>')  # any other path
def catch_all(path):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'dist/' + path)

    if os.path.isfile(filename):  # if path is a file, send it back
        return app.send_static_file(path)

    return app.send_static_file('index.html')
