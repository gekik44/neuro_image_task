from flask import Flask, render_template, request
from neuro import convert_image
from data import db_session
import random
from PIL import Image
from data.users import User
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///account.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db = SQLAlchemy(app)
#


@app.route("/")
def index():
    return render_template("index.html", title="start")

@app.route("/authorization")
def authorization():
    return render_template("authorization.html", title="authorization")
@app.route("/account")
def account():
    return render_template("account.html", title="account")
@app.route("/img_converter", methods=["GET", "POST"])
def img_converter():
    if request.method == "GET":
        return render_template("img_converter.html", title="converter")
    elif request.method == "POST":
        if request.form:
            style = request.form['radiostyle']
            image = request.form['radioimage']
            content_blending_ratio = 1 - float(request.form['content_blending_ratio'])

            image_style_path = f"static/img/{style}.jpg"
            content_image_path = f"static/img/{image}.jpg"
            if image == 'content_image_3':
                with open("static/txt/links_content.txt") as file:
                    line = file.read().split()
                content_image_path = random.choice(line)
            if style == 'image_style_7':
                with open("static/txt/links_style.txt") as file:
                    lines = file.read().split()
                image_style_path = random.choice(lines)
            convert_image(content_image_path, image_style_path, content_blending_ratio)
        return render_template("img_converter.html", title="converter")
    return render_template("img_converter.html", title="converter")


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    image = Image.new(mode="RGB", size=(256, 256), color="#452E1D")
    image.save("static/img/file.png")
    # user = User()
    # user.username = "Gelik4na4"
    # user.email = "1234@mail.ru"
    # user.hashed_password = "1234"
    # db_sess = db_session.create_session()
    # db_sess.add(user)
    # db_sess.commit()
    app.run()
    #app.run(host='192.168.0.100', port=8080)




