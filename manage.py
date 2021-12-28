import requests
import urllib.parse
import re

from flask import render_template, redirect, session
from functools import wraps


def prompt(message, code=400):
    """ Prompt error codes along with appropriate message """

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    return render_template("prompt.html", top=code, bottom=escape(message)), code


def login_required(f):
    """ Decorate routes to require login. """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def login_not_required(f):
    """ Decorate routes to not require login. """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id"):
            return redirect("/home")
        return f(*args, **kwargs)
    return decorated_function


def password_check(password):
    """ Check if the given password is valid """

    regExp = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,15}$"

    pattern = re.compile(regExp)

    isValid = re.search(pattern, password)

    return isValid


def searchByTitle(number, title):
    """ Looks up for a book by title """

    # Contact API
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{urllib.parse.quote_plus(title)}&maxResults={number}"
        response = requests.get(url)
        response.raise_for_status()

    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        quote = quote["items"]
        return quote
    except (KeyError, TypeError, ValueError):
        return None


def searchByAuthor(number, author, title=""):
    """ Looks up for a book by author and title if provided"""

    if not title:
        # Contact API
        try:
            url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{urllib.parse.quote_plus(author)}&maxResults={number}"
            response = requests.get(url)
            response.raise_for_status()

        except requests.RequestException:
            return None

    else:
        # Contact API
        try:
            url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{urllib.parse.quote_plus(title)}+inauthor:{urllib.parse.quote_plus(author)}&maxResults={number}"
            response = requests.get(url)
            response.raise_for_status()

        except requests.RequestException:
            return None

    # Parse response
    try:
        quote = response.json()
        quote = quote["items"]
        return quote
    except (KeyError, TypeError, ValueError):
        return None


def searchByISBN(isbn):
    """ Looks up for a book by isbn no """

    # Contact API
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{urllib.parse.quote_plus(isbn)}"
        response = requests.get(url)
        response.raise_for_status()

    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        quote = quote["items"]
        return quote
    except (KeyError, TypeError, ValueError):
        return None
