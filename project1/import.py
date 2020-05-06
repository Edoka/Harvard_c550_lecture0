import csv
import os

import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    table_name = 'booksx'
    for isb, tit, auth, yr in reader:
        db.execute("INSERT INTO table_name (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
            {"isbn": isb, "title": tit, "author": auth, "year": yr})
        print(tit)

    db.commit()
    bookInfos = []
    isbns = {}
    isbn_new = []
    # isbns = db.execute("SELECT isbn FROM table_name where reviews_count is null limit 1000").fetchall()
    isbns = db.execute("SELECT isbn FROM table_name where reviews_count is null").fetchall()
    for i in isbns:
        for isbn in i:
            isbn_new = isbn

            try:
                res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "0cupmLsyxu5s3kNUJCNXJg", "isbns": {isbn_new} })
                bookInfos = res.json()
                bookInfo = bookInfos['books'][0]
                res.raise_for_status()
                cUpdate = db.execute("UPDATE table_name SET reviews_count = :reviews_count, text_reviews_count = :text_reviews_count, work_ratings_count = :work_ratings_count, work_reviews_count = :work_reviews_count, work_text_reviews_count = :work_text_reviews_count, average_rating = :average_rating WHERE isbn = :isbn",
               {"reviews_count": bookInfo['reviews_count'], "text_reviews_count": bookInfo['text_reviews_count'], "work_ratings_count": bookInfo['work_ratings_count'], "work_reviews_count": bookInfo['work_reviews_count'], "work_text_reviews_count": bookInfo['work_text_reviews_count'], "average_rating": bookInfo['average_rating'], "isbn": bookInfo['isbn']})
                print(bookInfo['isbn'])
            except:
                # print(err)
                pass
    db.commit() 


if __name__ == "__main__":
    main()
