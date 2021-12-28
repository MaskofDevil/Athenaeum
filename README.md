# ATHENAEUM - A place for book lovers

#### Description:

Athenaeum is a web application that uses Google Books API to provide books as search results. For logged in users, it provides more information per each book and if the book happens to have a online readable version available then it is shown inside an embedded viewer. If the user is not logged in, it shows the search results as a list with very less information.

##### Project Structure:
    project/
    ├── static/
    |   ├── img/
    |   |   ├── book.png
    |   |   ├── no-book-cover.jpeg
    |   |   ├── search-not-found.png
    |   |   └── unable-to-load.png
    │   ├── favicon.ico
    │   └── styles.css
    ├── templates/
    |   ├── bookView.html
    |   ├── change.html
    |   ├── home.html
    |   ├── index.html
    |   ├── layout.html
    |   ├── login.html
    |   ├── prompt.html
    |   ├── register.html
    |   ├── search.html
    │   └── searchResults.html
    ├── app.py
    ├── athenaeum.db
    ├── Google_Books_API.http
    ├── manage.py
    ├── README.md
    └── requirements.txt

**app.py**
    Configure the app, Configure session to use filesystem (instead of signed cookies), Configure CS50 Library to use SQLite database, Listen and handle errors, Define routes:
        *index* *"/" route*-> 
            for **GET** request, simply shows "index.html" containing a search field and book.png
            for **POST** request, gets the submitted query, checks for errors(if error occurs, show using flash() method and redirects to "/" route), uses searchByTitle() method from "manage.py", renders results in "search.html"
        *login* *"/login" route*->
            clears session history,
            for **GET** request, shows "login.html" form containing a link to "/register" route if the user is not registered
            for **POST** request, gets the submitted form fields, validation check(if error occurs, flash() message and redirects to "/login" route to resubmit the form), creates user session and logs user in and redirects user to "/home" route
        *register* *"/register" route*->
            clears session history,
            for **GET** request, shows "register.html" form containing a link to "/login" route if the user already have an account
            for **POST** request, gets the submitted form, validation check and parameter check using password_check() method in "manage.py"(handles errors) and also checks if username is taken or not from "athenaeum.db", generates password hash and stores it in the database, creates user session and registers user and redirects user to "/home" route
        *logout* *"/logout" route*->
            checks if user is logged in using "@login_required" from manage.py
            clears session history, redirects user to "/" route
        *change* *"/change" route*->
            checks if user is logged in using "@login_required"
            for **GET** request, shows the "change.html" form
            for **POST** request, performs validation check and parameter check and logs the user out
        *home* *"/home" route*->
            checks if user is logged in using "@login_required"
            for **GET** request, greets the user and shows "home.html"
            for **POST** request, gets different fields to perform searchByTitle(), searchByAuthor(), searchByISBN() method from "manage.py" and shows the results in "searchResults.html"
        *bookView* *"/bookview" route*
            checks if user is logged in using "@login_required"
            for **GET** request, shows "bookView.html"
            for **POST** request, previews book if available using Google Books Embedded Viewer otherwise shows description(handles errors)

**manage.py**
    Define utility functions such as -
        *prompt()*-> prompts error message
        *login_required()*-> decorate routes to require login
        *login_not_required()*-> decorate routes not to go back to the index page
        *password_check()*-> validates password using regular expression
        *searchByTitle()*-> provides books by book title by requesting to Google Books API
        *searchByAuthor()*-> provides books by author and title(if provided) by requesting to Google Books API
        *searchByISBN()*-> provides books by ISBN no. by requesting to Google Books API

**athenaeum.db**
    Contain users table which has username, password hash

**requirements.txt**
    Lists the packages to run the project
    * The system must have latest version of python and pip installed
    * The version of python to develop this project is python 3.10
    Run ``` pip install -r requirements.txt ``` to install the requirements

**layout.html**
    links "favicon.ico", "styles.css", loads bootstrap, jQuery, Google Books API Loader Library(the script to use the library is in "bookView.html"), contains a script to automatically close flash alert messages and a generalized layout for all the other templates in the "templates" directory

##### Built with
* Flask
* sqlite3
* HTML
* CSS
* Bootstrap
* jQuery
* Figma (UI design)

##### Future scopes:
1. Add pagination
2. Add recommendation system