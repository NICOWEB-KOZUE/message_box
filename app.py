# from flask import Flask, flash, redirect, render_template, request
# from flask_login import LoginManager, login_user
# from werkzeug.security import generate_password_hash, check_password_hash
# from config import User

# app = Flask(__name__)
# app.secret_key = "secret"
# login_manager = LoginManager()
# login_manager.init_app(app)


# # Flask-Loginがユーザー情報を取得するためのメソッド
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get_by_id(user_id)


# # ユーザー登録フォーム
# @app.route('/register', methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         # 未入力のときの処理
#         if not request.form["name"] or not request.form["password"] or not request.form["email"]:
#             flash("未入力の項目があります。")
#             return redirect(request.url)
#         # データの重複
#         if User.select().where(User.name == request.form["name"]):
#             flash("その名前はすでに使われています。")
#             return redirect(request.url)
#         if User.select().where(User.email == request.form["email"]):
#             flash("そのメールアドレスはすでに使われています。")
#             return redirect(request.url)

#         # ユーザー登録
#         User.create(
#             name=request.form["name"],
#             email=request.form["email"],
#             password=generate_password_hash(request.form["password"]),
#         )
#         return render_template("index.html")

#     return render_template("register.html")


# # ログインフォームの表示・ログイン処理
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         # データの検証
#         if not request.form["password"] or not request.form["email"]:
#             flash("未入力の項目があります。")
#             return redirect(request.url)

#         # ログイン処理をここに書く！
#         user = User.select().where(User.email == request.form["email"]).first()
#         if user is not None and check_password_hash(user.password, request.form["password"]):
#              login_user(user)
#              flash(f"ようこそ！ {user.name} さん")
#              return redirect("/")

#         # NGならフラッシュメッセージを返す
#         flash("認証に失敗しました")

#     return render_template("login.html")


# @app.route('/')
# def index():
#     return render_template('index.html')


# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=8000, debug=True)

from flask import Flask, render_template, request, redirect, flash
from flask_login import LoginManager, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import User

app = Flask(__name__)
app.secret_key = "secret"

login_manager = LoginManager()
login_manager.init_app(app)


# Flask-Loginがユーザー情報を取得するためのメソッド
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # 未入力のときの処理
        if not request.form["name"] or not request.form["password"] or not request.form["email"]:
            flash("未入力の項目があります。")
            return redirect(request.url)

        # データの重複
        if User.select().where(User.name == request.form["name"]):
            flash("その名前はすでに使われています!")
            return redirect(request.url)
        if User.select().where(User.email == request.form["email"]):
            flash("そのメールアドレスはすでに使われています!")
            return redirect(request.url)

        User.create(
            name=request.form["name"],
            email=request.form["email"],
            password=generate_password_hash(request.form["password"]),
        )
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # データを検証
        if not request.form["password"] or not request.form["email"]:
            flash("未入力の項目があります。")
            return redirect(request.url)

        # ログイン処理をここに書く!
        user = User.select().where(User.email == request.form["email"]).first()
        if user is not None and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            flash(f"ようこそ{user.name}さん")
            return redirect("/")

        # だめだったとき
        flash("認証に失敗しました")

    return render_template("login.html")


# ログアウト処理
@app.route("/logout")
def logout():
    logout_user()
    flash("ログアウトしました！")
    return redirect("/")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
