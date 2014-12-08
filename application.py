from flask import Flask, render_template
from results import json_ready_chart
from labels import labels


app = Flask(__name__)


@app.route("/")
def root():
    return render_template('index.html')


@app.route("/results")
def results():
    return render_template(
        'results.html',
        json_data=json_ready_chart('csv/bankaustria.csv', labels))

if __name__ == "__main__":
    # XXX make this configurable
    app.config['DEBUG'] = True
    app.run()
