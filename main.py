from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="start")

@app.route("/img_converter")
def img_converter():
    return render_template("img_converter.html", title="converter")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)






