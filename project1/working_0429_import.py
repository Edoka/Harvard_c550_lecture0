import csv
import os

import requests

# from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
# from flask_sqlalchemy import SQLAlchemy

# engine = create_engine(os.getenv("postgresql:///mez"))
engine = create_engine(os.getenv("DATABASE_URL"))
# engine = create_engine("postgresql://mez")
db = scoped_session(sessionmaker(bind=engine))
# db = SQLAlchemy(app)

# class Bookss(db.Model):
#     __tablename__ ='bookss'
#     id = db.Column('id', db.Integer, primary_key=True)
#     isbn = db.Column('isbn', db.VARCHAR)
#     title = db.Column('title', db.VARCHAR)
#     author = db.Column('author', db.VARCHAR)
#     year = db.Column('year', db.VARCHAR)
#     isbn13 = db.Column('isbn13', db.Integer)
#     reviews_count = db.Column('reviews_count', db.Integer)
#     text_reviews_count = db.Column('text_reviews_count', db.Integer)
#     work_ratings_count = db.Column('work_ratings_count', db.Integer)
#     work_reviews_count = db.Column('work_reviews_count', db.Integer)
#     work_text_reviews_count = db.Column('iwork_text_reviews_countsbn13', db.Integer)
#     average_rating = db.Column('average_rating', db.Integer)

    # def __init__(self, id, title, author, year, isbn13, reviews_count, text_reviews_count, work_ratings_count, work_reviews_count, average_rating )
    #     self.id = id
    #     self.isbn = isbn
    #     self.title = title
    #     self.author = author
    #     self.year = year
    #     self.isbn13 = isbn13
    #     self.reviews_count = reviews_count
    #     self.text_reviews_count = text_reviews_count
    #     self.work_ratings_count = work_ratings_count
    #     self.work_reviews_count = work_reviews_count
    #     self.work_text_reviews_count = work_text_reviews_count
    #     self.average_rating = average_rating

def main():
    # f = open("books.csv")
    # reader = csv.reader(f)
    # for isb, tit, auth, yr in reader:
    #     db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
    #         {"isbn": isb, "title": tit, "author": auth, "year": yr})
        # print(f"From {books.isbn} to {books.title} will take {books.author} minutes").fetchall()

    # for books in bookss:
    #     print(f"Added books from {origin} to {destination} lasting {duration} minutes.")
    # db.commit()
    bookInfos = []
    isbns = {}
    isbn_new = []
    # isbns = {9781529408928}
    isbns = db.execute("SELECT isbn FROM books where reviews_count is null limit 10").fetchall()
    # isbns = db.execute("SELECT isbn FROM books ").fetchall()
    # isbns = {9781529408928,1632168146,9780593237724}
    for i in isbns:
        for isbn in i:
            isbn_new = isbn
            # print(isbn_new)

            # res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "0cupmLsyxu5s3kNUJCNXJg", "isbns": {isbn_new} })

            res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "0cupmLsyxu5s3kNUJCNXJg", "isbns": {isbn_new} })
            bookInfos = res.json()
            bookInfo = bookInfos['books'][0]
            # for x in bookInfo:
            #     print(x)
            # for k, v in bookInfo.items():
            #     print("%s: %s" % (k, v))

            cUpdate = db.execute("UPDATE books SET reviews_count = :reviews_count, text_reviews_count = :text_reviews_count, work_ratings_count = :work_ratings_count, work_reviews_count = :work_reviews_count, work_text_reviews_count = :work_text_reviews_count, average_rating = :average_rating WHERE isbn = :isbn",
            {"reviews_count": bookInfo['reviews_count'], "text_reviews_count": bookInfo['text_reviews_count'], "work_ratings_count": bookInfo['work_ratings_count'], "work_reviews_count": bookInfo['work_reviews_count'], "work_text_reviews_count": bookInfo['work_text_reviews_count'], "average_rating": bookInfo['average_rating'], "isbn": bookInfo['isbn']})
            # cUpdate = db.execute("UPDATE books SET reviews_count = :reviews_count, text_reviews_count = :text_reviews_count, work_ratings_count = :work_ratings_count, work_reviews_count = :work_reviews_count, work_text_reviews_count = :work_text_reviews_count, average_rating = :average_rating WHERE isbn = '0380795272'",
            #     {"reviews_count": = bookInfo['reviews_count'], "text_reviews_count": bookInfo['text_reviews_count'], "work_ratings_count": bookInfo['work_ratings_count'], "work_reviews_count": bookInfo['work_reviews_count'], "work_text_reviews_count": bookInfo['work_text_reviews_count'], "average_rating": bookInfo['average_rating']).fetchall()

            # update_user =  db.bookss.query.filter_by(isbn = '0380795272').first()
            # ("UPDATE books SET reviews_count = :reviews_count, text_reviews_count = :text_reviews_count, work_ratings_count = :work_ratings_count, work_reviews_count = :work_reviews_count, work_text_reviews_count = :work_text_reviews_count, average_rating = :average_rating WHERE isbn = '0380795272'",

            # print(bookInfo['isbn'])
            print(bookInfo['isbn'])
    db.commit()    

    # print(isbn[4][0])
        # print(bookInfo['books'][0]['reviews_count'])
        # print(f"INSERT INTO books (title, author, year, isbn, reviews_count, average_rating) VALUES ('Memory', 'Doug Lloyd', 2015, '1632168146', 28, 5.0);",
    # #         {"origin": or, "destination": dest, "duration": dur}))



if __name__ == "__main__":
    main()
