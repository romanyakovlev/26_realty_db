from flask import Flask, render_template, request, url_for
from app import app
from models import Apartment
from math import ceil
from werkzeug.contrib.cache import SimpleCache


cache = SimpleCache()
POSTS_PER_PAGE = 15

@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def homepage(page):
    apartments = Apartment.query

    if request.args.get('oblast_district'):
        cache.set('oblast_district', request.args.get('oblast_district'))
        cache.delete('min_price')
        cache.delete('max_price')
        apartments = apartments.filter(Apartment.oblast_district == request.args.get('oblast_district'))
    else:
        oblast_district_cache = cache.get('oblast_district')
        if oblast_district_cache:
            apartments = apartments.filter(Apartment.oblast_district == oblast_district_cache)

    if bool(request.args.get('min_price')):
        cache.set('min_price', request.args.get('min_price'))
        apartments = apartments.filter(Apartment.price >= int(request.args.get('min_price')))
    else:
        min_price_cache = cache.get('min_price')
        if min_price_cache:
            apartments = apartments.filter(Apartment.oblast_district >= min_price_cache)

    if bool(request.args.get('max_price')):
        print('kek')
        cache.set('max_price', request.args.get('max_price'))
        apartments = apartments.filter(Apartment.price <= int(request.args.get('max_price')))
    else:
        max_price_cache = cache.get('max_price')
        if max_price_cache:
            apartments = apartments.filter(Apartment.oblast_district <= max_price_cache)

    count = apartments.count()
    posts = apartments.paginate(page, POSTS_PER_PAGE, count)
    print(request.args.get('oblast_district'), bool(request.args.get('max_price')), bool(request.args.get('min_price')))

    return render_template('ads_list.html', pagination=posts)


if __name__ == "__main__":
    app.run(port=3000)
