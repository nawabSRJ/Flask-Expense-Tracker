from flask import render_template, url_for
from app import create_app

app = create_app()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)