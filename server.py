from flask import render_template, request
from main import app
from models import Apartment
from sqlalchemy.sql import func
from datetime import date


POSTS_PER_PAGE = 15
year_limit = 2


def apartments_filter(get_params, apartments):
    if get_params.get('oblast_district'):
        apartments = apartments.filter(Apartment.oblast_district == get_params.get('oblast_district')[0])
    if get_params.get('min_cost'):
        apartments = apartments.filter(Apartment.price >= get_params.get('min_cost')[0])
    if get_params.get('max_cost'):
        apartments = apartments.filter(Apartment.price <= get_params.get('max_cost')[0])
    if get_params.get('new_building'):
        current_year = date.today().year
        apartments = apartments.filter(Apartment.under_construction == True).filter(
                     current_year - Apartment.construction_year <= year_limit)

    return apartments


@app.route('/', defaults={'page': 1})
@app.route('/<int:page>')
def ads_list(page):
    apartments = Apartment.query
    all_get_params  = dict(request.args)
    not_null_get_params = {param_key: all_get_params[param_key] for param_key in all_get_params.keys()
                           if all_get_params[param_key][0] is not ''}
    apartments = apartments_filter(not_null_get_params, apartments)
    count = apartments.count()
    posts = apartments.paginate(page, POSTS_PER_PAGE, count)

    return render_template('ads_list.html', pagination=posts, get_params=not_null_get_params)


if __name__ == "__main__":
    app.run(port=3000)
