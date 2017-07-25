from flask import render_template, request
from main import app
from models import Apartment

POSTS_PER_PAGE = 15


@app.route('/', defaults={'page': 1})
@app.route('/<int:page>')
def ads_list(page):

    form_advert_info = dict()
    apartments = Apartment.query

    if request.args.get('oblast_district'):
        form_advert_info_advert_info['oblast_district'] = request.args.get('oblast_district')
        apartments = apartments.filter(Apartment.oblast_district == form_advert_info['oblast_district'])

    if request.args.get('new_building'):
        form_advert_info['new_building'] = bool(request.args.get('new_building'))
        apartments = apartments.filter(Apartment.active == form_advert_info['new_building'])

    if request.args.get('min_cost'):
        form_advert_info['min_cost'] = request.args.get('min_cost')
        apartments = apartments.filter(Apartment.price >= form_advert_info['min_cost'])

    if request.args.get('max_cost'):
        form_advert_info['max_cost'] = request.args.get('max_cost')
        apartments = apartments.filter(Apartment.price <= form_advert_info['max_cost'])

    count = apartments.count()
    posts = apartments.paginate(page, POSTS_PER_PAGE, count)

    return render_template('ads_list.html', pagination=posts, form=form_advert_info)


if __name__ == "__main__":
    app.run(port=3000)
