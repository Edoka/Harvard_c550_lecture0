import os
import time #Heroku dev verion does not allow more than 1 query within 2 seconds 

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods=['GET', 'POST'])
def index():
    # status = False
    # username = ''
    # user_id = 0
    message = ''
    if 'logged_in' in session:
        status = session['logged_in']
        user_id = session['user_id']
        username = session['username']
        message = f"Welcome, {username}."
    return render_template("index.html", status=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # global username
    session['user_id'] = []
    session['username'] = []
    session['logged_in'] = []
    username = request.form.get("name")
    error = "Username or password is wrong. Please try again"
    session['logged_in'] = False
    username_entered = request.form.get("name")
    email_entered = request.form.get("email")
    password_entered = request.form.get("pwd")

    if request.method == 'POST':
        if username_entered != '' and password_entered != '': #check if username or password is empty
            newUser = db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)", 
                {"username": username_entered, "email": email_entered, "password": password_entered})
            db.commit()
            time.sleep(2)

            profile = db.execute("SELECT user_id, username, email, password FROM users WHERE username = :username AND password = :password", 
                {"username": username_entered, "password": password_entered}).fetchall()
        
            if profile != []:
                session['logged_in'] = True
                message = f"Welcome { username_entered }"
                return redirect(url_for('profile'))
    return render_template('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = "Username or password is wrong. Please try again"
    session['user_id'] = []
    session['username'] = []
    session['logged_in'] = []
    username_entered = request.form.get("name")
    password_entered = request.form.get("pwd")
    if request.method == 'POST':
        profile = db.execute("SELECT user_id, username, email, password FROM users WHERE username = :username AND password = :password", 
            {"username": username_entered, "password": password_entered}).fetchall()
        
        if profile:
            session['logged_in'] = True
            session['user_id'] = profile[0][0]
            session['username'] = username_entered
            message = f"Welcome { session['username'] }"
            return redirect(url_for('profile'))
    return render_template('login.html', error=session['logged_in'])


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect('/')


@app.route("/books", methods=['GET', 'POST'])
def profile():
    username = session['username']
    page_name = "login"
    message = "Username or password is wrong. Please try again"

    if session.get('logged_in'):
        message = f"Welcome { username }"
        page_name = "profile"
        # page_name "login"
    # return render_template("profile.html", user_id=message)
    return render_template("%s.html" %page_name, message=message)


# @app.route("/b/<string:isbn>", methods=['GET', 'POST'])
@app.route("/b", methods=["POST"])
def books():
    isbn_entered = request.form.get("isbn")
    review_entered = request.form.get("review")
    review_text_entered = request.form.get("review_text")

    if request.method == 'POST':
        if session['logged_in']:
            bookk = db.execute("SELECT json_agg(to_json(b)) FROM (SELECT id, title, author, year, isbn, reviews_count, average_rating FROM books WHERE isbn like :isbn OR title = :isbn OR author = :isbn) as b", 
            {"isbn": isbn_entered}).fetchall()
            if bookk != []:
                bookk = bookk[0][0][0]
                message = bookk
                title = bookk['title']
                author = bookk['author']
                year = bookk['year']
                isbn = bookk['isbn']
                reviews_count = bookk['reviews_count']
                average_rating = bookk['average_rating']

                review = db.execute("SELECT user_id, review_entered, review_text_entered, isReviewed FROM reviews WHERE user_id = :user_id AND isbn = :isbn", 
                    {"user_id": session['user_id'],"isbn": isbn}).first()
                if not review:
                    session['isReviewed'] = False
                else:
                    book_review = review[1]
                    book_review_text = review[2]
                    session['isReviewed'] = review[3]
            return render_template("books.html", bookk=review, title=title, author=author, year=year, isbn=isbn, reviews_count=reviews_count, average_rating=average_rating, book_review=book_review, book_review_text=book_review_text)

    return render_template("login.html", bookk=session['logged_in'])


@app.route("/b/review/<string:isbn>", methods=['GET', 'POST'])
def book(isbn):
    isReviewed = False
    user_id = session['user_id']
    review_entered = request.form.get("review")
    review_text_entered = request.form.get("review_text")
    if session['logged_in']:   
        review = db.execute("SELECT review_entered, review_text_entered, isReviewed FROM reviews WHERE user_id = :user_id AND isbn = :isbn", 
            {"user_id": user_id, "isbn": isbn}).first()

        if not review:
            addReview = db.execute("INSERT INTO reviews (user_id, isbn, review_entered, review_text_entered, isReviewed) VALUES (:user_id, :isbn, :review_entered, :review_text_entered, :isReviewed)", 
                {"user_id": user_id, "isbn": isbn, "review_entered": review_entered, "review_text_entered": review_text_entered, "isReviewed": True})
            db.commit()
        db.commit()
    return f"Review entered for {isbn}: {review_entered}. While review saved to DB is: {review}"

