from flask import Flask, render_template, request
from neuro import convert_image


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="start")

@app.route("/img_converter", methods=["GET", "POST"])
def img_converter():
    if request.method == "GET":
        return render_template("img_converter.html", title="converter")
    elif request.method == "POST":
        print(request.form)
        if request.form['image_style_1'] == 'on':
            convert_image("image_style_1.jpg")
        return render_template("img_converter.html", title="converter")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)






