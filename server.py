from flask import Flask, render_template, request, url_for
from app import app
from models import Apartment
from math import ceil


POSTS_PER_PAGE = 15
@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def homepage(page):
  count = Apartment.query.count()
  posts = Apartment.query.paginate(page, POSTS_PER_PAGE, count)
  return render_template('ads_list.html', pagination=posts)



if __name__ == "__main__":
    app.run(port=3000)
