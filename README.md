# ATHENAEUM - A place for book lovers

#### Description:

Athenaeum is a web application that uses Google Books API to provide books as search results. For logged in users, it provides more information per each book and if the book happens to have a online readable version available then it is shown inside an embedded viewer. If the user is not logged in, it shows the search results as a list with very less information.

---

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

---

* Search books without logging in:
    <br />
    ![Search without Login](https://user-images.githubusercontent.com/66861616/147540252-7b98f896-3b08-4c96-8680-93a149d4cf6f.gif)

* Search books by name and read:
    <br />
    ![Search by name and read](https://user-images.githubusercontent.com/66861616/147540314-24c8b21b-07a5-4090-88dd-88a51053bf76.gif)

* Search books by author:
    <br />
    ![Search by author](https://user-images.githubusercontent.com/66861616/147540345-6f99a666-c982-4dee-9fe0-b6cda9548d11.gif)

* Search book by ISBN no:
    <br />
    ![Search by ISBN](https://user-images.githubusercontent.com/66861616/147540383-3479cc8e-d3d4-4749-a1e5-98450f01b18a.gif)

---

##### Built with
* Flask
* sqlite3
* HTML
* CSS
* Bootstrap
* jQuery
* Figma (UI design)

---

##### Future scopes:
1. Add recommendation system

### ⭐ Star this repo
