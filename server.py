from flask import render_template, request
from main import app
from models import Apartment
from sqlalchemy.sql import func

POSTS_PER_PAGE = 15

def apartments_filter(form):
    if form['']

@app.route('/', defaults={'page': 1})
@app.route('/<int:page>')
def ads_list(page):
    apartments = Apartment.query

    apartments = apartments.filter(Apartment.oblast_district == oblast_district)
    if new_building:
        apartments = apartments.filter(Apartment.active == new_building)
    apartments = apartments.filter(Apartment.price >= min_cost)
    apartments = apartments.filter(Apartment.price <= max_cost)
    kek = dict(request.args)
    count = apartments.count()
    posts = apartments.paginate(page, POSTS_PER_PAGE, count)

    return render_template('ads_list.html', pagination=posts,
                                            form={k:kek[k] for k in kek.keys() if kek[k][0] is not ''})


if __name__ == "__main__":
    app.run(port=3000)
