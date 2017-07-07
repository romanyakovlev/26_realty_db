from flask import Flask, render_template, request, url_for
from app import app
from models import Apartment
from math import ceil
from werkzeug.contrib.cache import SimpleCache
from forms import PastebinEntry

cache = SimpleCache()
POSTS_PER_PAGE = 15


@app.route('/', defaults={'page':1})
@app.route('/<int:page>')
def submit(page):
    form = PastebinEntry()
    if request.args.get('language'):
        form.language.data = request.args.get('language')
    if not request.args.get('new_building'):
        form.new_building.data = False
    if request.args.get('min_cost'):
        form.min_cost.data = request.args.get('min_cost')
    if request.args.get('max_cost'):
        form.max_cost.data = request.args.get('max_cost')

    apartments = Apartment.query
    apartments = apartments.filter(Apartment.oblast_district == form.language.data)
    apartments = apartments.filter(Apartment.price >= form.min_cost.data)
    apartments = apartments.filter(Apartment.price <= form.max_cost.data)
    count = apartments.count()
    posts = apartments.paginate(page, POSTS_PER_PAGE, count)
    print(form.data)
    return render_template('ads_list.html', pagination=posts, form=form)


if __name__ == "__main__":
    app.run(port=3000)
