from flask import render_template, request
from main import app
from models import Apartment
from sqlalchemy.sql import func

POSTS_PER_PAGE = 15


@app.route('/', defaults={'page': 1})
@app.route('/<int:page>')
def ads_list(page):

    apartments = Apartment.query

    oblast_district = request.args.get('oblast_district', 'Череповецкий район')
    new_building = request.args.get('new_building', None)

    apartments = apartments.filter(Apartment.oblast_district == oblast_district)
    if new_building:
        apartments = apartments.filter(Apartment.active == new_building)

    min_cost = request.args.get('min_cost', 0)
    max_cost = request.args.get('max_cost', apartments.order_by(Apartment.price)[-1].price if
                                                                len(apartments.all()) != 0 else 0)

    apartments = apartments.filter(Apartment.price >= min_cost)
    apartments = apartments.filter(Apartment.price <= max_cost)

    print(request.args)

    count = apartments.count()
    posts = apartments.paginate(page, POSTS_PER_PAGE, count)

    return render_template('ads_list.html', pagination=posts,
                                            form={})


if __name__ == "__main__":
    app.run(port=3000)
