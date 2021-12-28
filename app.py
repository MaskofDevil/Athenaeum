from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# manage.py
from manage import prompt, login_required, login_not_required, password_check, searchByTitle, searchByAuthor, searchByISBN

# Configure app
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///athenaeum.db")


@app.route("/", methods=["GET", "POST"])
@login_not_required
def index():
    """ Show landing page """

    if request.method == "POST":

        q = request.form.get("q")

        if not q:
            flash("Please enter a book name", "alert-warning")
            return redirect("/")

        q = searchByTitle(30, q)

        if q:
            flash("Login to read books", "alert-info")
            return render_template("search.html", q=q)

        else:
            flash("Invalid Search", "alert-danger")
            return redirect("/")

    else:
        return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
@login_not_required
def login():
    """ Show login form """

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            flash("Must provide a Username", "alert-warning")
            return render_template("login.html")

        elif not request.form.get("password"):
            flash("Must provide Password", "alert-warning")
            return render_template("login.html")

        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid Username and/or Password", "alert-danger")
            return render_template("login.html")

        session["user_id"] = rows[0]["id"]
        flash("Successfully logged in!", "alert-success")
        return redirect("/home")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
@login_not_required
def register():
    """ Show register form """

    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        cpassword = request.form.get("confirm_password")

        if not username:
            flash("Must provide a Username", "alert-warning")
            return render_template("register.html")

        if not password:
            flash("Must provide a Password", "alert-warning")
            return render_template("register.html")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) == 1:
            flash("Username is taken", "alert-danger")
            return render_template("register.html")

        if not password == cpassword:
            flash("Passwords doesn't match", "alert-warning")
            return render_template("register.html")

        if not password_check(password):
            flash("Password doesn't satisfy parameters", "alert-warning")
            return render_template("register.html")

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                   username, generate_password_hash(password))
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]
        flash("Successfully registered!", "alert-success")
        return redirect("/home")

    else:
        return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    session.clear()
    flash("Successfully logged out!", "alert-success")
    return redirect("/")


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Change password"""

    if request.method == "POST":

        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        cpassword = request.form.get("confirm_password")

        if not old_password:
            flash("Must provide old password", "alert-warning")
            return render_template("change.html")

        if not new_password:
            flash("Must provide a new password", "alert-warning")
            return render_template("change.html")

        if old_password == new_password:
            flash("New password is same as old password", "alert-danger")
            return render_template("change.html")

        if not new_password == cpassword:
            flash("Passwords doesn't match", "alert-warning")
            return render_template("change.html")

        if not password_check(new_password):
            flash("Password doesn't satisfy parameters", "alert-warning")
            return render_template("change.html")

        db.execute("UPDATE users SET hash = ? WHERE id = ?",
                   generate_password_hash(new_password), session["user_id"])
        session.clear()
        flash("Password change successful! Login again", "alert-success")
        return redirect("/")

    else:
        return render_template("change.html")


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    """ Show user homepage """

    if request.method == "POST":

        name = request.form.get("name")
        author = request.form.get("author")
        isbn = request.form.get("isbn")

        # Ensure user entered any of the input fields
        if isbn:
            booksByISBN = searchByISBN(isbn)
            return render_template("searchResults.html", q=booksByISBN)

        if not (name or author or isbn):
            flash("Please enter a book name or author or isbn", "alert-info")
            return redirect("/home")

        if name and author:
            booksByNameAndAuthor = searchByAuthor(40, author, name)
            return render_template("searchResults.html", q=booksByNameAndAuthor)

        if name:
            booksByName = searchByTitle(40, name)
            return render_template("searchResults.html", q=booksByName)

        if author:
            booksByAuthor = searchByAuthor(40, author)
            return render_template("searchResults.html", q=booksByAuthor)

    else:
        user = db.execute(
            "SELECT username FROM users WHERE id = ?", session["user_id"])
        user = user[0]["username"]
        return render_template("home.html", user=user)


@app.route("/bookview", methods=["GET", "POST"])
@login_required
def bookView():
    """ Shows book if available """

    if request.method == "POST":
        isbn = request.form.get("isbn")
        if isbn:
            return render_template("bookView.html", isbn=isbn)

        description = request.form.get("description")
        if description:
            return render_template("bookView.html", description=description)

        else:
            prompt("Something unexpected happened")

    else:
        return render_template("bookView.html")


def errorhandler(e):
    """Handle error"""

    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return prompt(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
