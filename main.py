from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def start_page():
    return render_template("start.html", title="start")

@app.route("/carousel")
def carousel_page():
    return render_template("carousel.html", title="carousel")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)






