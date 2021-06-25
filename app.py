from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app: Flask = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db: SQLAlchemy = SQLAlchemy(app)


class games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return f'{self.id} Game Name:{self.name}; Publisher: {self.publisher}'


@app.route("/")
def home():
    all_games = games.query.all()
    return render_template('index.html', all_games=all_games)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin123':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('view'))
    return render_template('login.html', error=error)


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out")
    return redirect(url_for("login"))


@app.route("/view")
def view():
    return render_template("view.html")


@app.route("/games", methods={'GET', 'POST'})
def games():
    if request.method == 'POST':
        n = request.form['name']
        i = request.form['id']
        p = request.form['publisher']
        g1 = games(name=n, id=i, publisher=p)
        db.session.add(g1)
        db.commit()
        flash ('Game successfully added')
    return render_template('games.html')


if __name__ == '__main__':
    app.run(debug=True)
