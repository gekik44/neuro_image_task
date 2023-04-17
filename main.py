from flask import Flask, render_template, request
from neuro import convert_image
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///account.db'
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
        print(request.form)
        if request.form:
            style = request.form['radiostyle']
            image = request.form['radioimage']
            content_blending_ratio = 1 - float(request.form['content_blending_ratio'])
            if image == 'content_image_1':
                content_image = "content_image_1.jpg"
            elif image == 'content_image_2':
                content_image = "content_image_2.jpg"
            elif image == 'content_image_3':
                content_image = "content_image_3.jpg"
            print(request.form)
            if style == 'image_style_1':
                convert_image(content_image, "image_style_1.jpg", content_blending_ratio)
            elif style == 'image_style_2':
                convert_image(content_image, "image_style_2.jpg", content_blending_ratio)
            elif style == 'image_style_3':
                convert_image(content_image, "image_style_3.jpg", content_blending_ratio)
            elif style == 'image_style_4':
                convert_image(content_image, "image_style_4.jpg", content_blending_ratio)
            elif style == 'image_style_5':
                convert_image(content_image, "image_style_5.jpg", content_blending_ratio)
            elif style == 'image_style_6':
                convert_image(content_image, "image_style_6.jpg", content_blending_ratio)
        return render_template("img_converter.html", title="converter")
    return render_template("img_converter.html", title="converter")


if __name__ == '__main__':
    app.run(host='192.168.0.100', port=8080)




