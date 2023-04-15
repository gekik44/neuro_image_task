from flask import Flask, render_template, request
from neuro import convert_image
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite:///account.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db = SQLAlchemy(app)
#
# class Account(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, primary_key=True, nullable=False)
#     email = db.Column(db.String, primary_key=True, nullable=False)
#     password = db.Column(db.String, nullable=False)
#     def __repr__(self):
#         return '<Account %r>'% self.id

@app.route("/")
def index():
    return render_template("index.html", title="start")

@app.route("/authorization")
def account():
    return render_template("authorization.html", title="authorization")
# @app.route("/account")
# def account():
#     return render_template("account.html", title="account")
@app.route("/img_converter", methods=["GET", "POST"])
def img_converter():
    if request.method == "GET":
        return render_template("img_converter.html", title="converter")
    elif request.method == "POST":
        if 'content_image_1' in request.form:
            content_image = "content_image_1.jpg"
        elif 'content_image_2' in request.form:
            content_image = "content_image_2.jpg"
        elif 'content_image_3' in request.form:
            content_image = "content_image_3.jpg"
        print(request.form)
        if 'image_style_1' in request.form:
            convert_image(content_image, "image_style_1.jpg")
        elif 'image_style_2' in request.form:
            convert_image(content_image, "image_style_2.jpg")
        elif 'image_style_3' in request.form:
            convert_image(content_image, "image_style_3.jpg")
        elif 'image_style_4' in request.form:
            convert_image(content_image, "image_style_4.jpg")
        elif 'image_style_5' in request.form:
            convert_image(content_image, "image_style_5.jpg")
        elif 'image_style_6' in request.form:
            convert_image(content_image, "image_style_6.jpg")
        return render_template("img_converter.html", title="converter")


if __name__ == '__main__':
    app.run(host='192.168.0.100', port=8080)






