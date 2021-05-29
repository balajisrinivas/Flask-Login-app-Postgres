from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from log_app import log

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application
# https://pypi.org/project/Flask-SQLAlchemy/

# log4py
log = log()
log.setLevel("DEBUG")  # DEBUG, INFO, WARNING, CRITICAL, ERROR
log.propagate = True  # Set to True if console printing is needed

app = Flask(__name__)
app.secret_key = "thisisasecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/postgres'
log.info('Connected to the postgres database')
db = SQLAlchemy(app)


class UserTable(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


db.create_all()
log.info("Tables created successfully")


@app.route('/home')
def home():
    if "username" in session:
        log.info("Entered the home page")
        return render_template("home.html")
    else:
        log.info("User accessed home page without session details and redirected back to login page")
        return redirect(url_for('login'))


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        log.info(f"Data entered into the login page, username is {username}, and password is {password}")

        login_val = UserTable.query.filter_by(username=username, password=password).first()
        log.info(f"Login validation returned {login_val}")

        if login_val:
            session["username"] = username
            log.info("Validation successful. Entering in to the next page")
            return redirect(url_for('home'))
        else:
            log.warning("Validation incorrect. Redirecting to the login page.")
            return render_template("login.html")
    else:
        log.info("Landed in the Login Page (GET Method)")
        return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_username = request.form["new_username"]
        new_email = request.form["new_email"]
        new_password = request.form["new_password"]

        log.info("Fetched data from the registration form")

        user_added = UserTable(username=new_username, email=new_email, password=new_password)
        db.session.add(user_added)
        db.session.commit()

        log.info(f"New user added. {new_username}, {new_email}, {new_password} to the database!!")

        return f"<h1>Registration success</h1>"
    else:
        log.info("Landed on the NEW USER REGISTRATION page")
        return render_template("register.html")


@app.route('/logout')
def logout():
    if "username" in session:
        session.pop("username")
        log.info("Removed the session details after logout")
    log.info("Logout successful")
    return redirect(url_for("login"))


if __name__ == "__main__":
    log.info("Entering into app successfully")
    app.run(debug=True)
