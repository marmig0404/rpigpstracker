from flask import Flask, render_template

from plot_service import generate_new_plot

PLOT_NAME = "plot"

app = Flask(__name__)


@app.route('/')
def index():
    generate_new_plot("templates/" + PLOT_NAME)
    return render_template(PLOT_NAME + ".html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
