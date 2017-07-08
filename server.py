from flask import render_template, request
from main import app
from models import Apartment
from forms import ApartmentListForm

POSTS_PER_PAGE = 15


@app.route('/', defaults={'page': 1})
@app.route('/<int:page>')
def ads_list(page):
    form = ApartmentListForm()

    if request.args.get('oblast_district'):
        form.oblast_district.data = request.args.get('oblast_district')
    if request.args.get('new_building'):
        form.new_building.data = bool(request.args.get('new_building'))
    if request.args.get('min_cost'):
        form.min_cost.data = request.args.get('min_cost')
    if request.args.get('max_cost'):
        form.max_cost.data = request.args.get('max_cost')

    apartments = Apartment.query
    apartments = apartments.filter(Apartment.oblast_district == form.oblast_district.data)
    apartments = apartments.filter(Apartment.price >= form.min_cost.data)
    apartments = apartments.filter(Apartment.price <= form.max_cost.data)
    count = apartments.count()
    posts = apartments.paginate(page, POSTS_PER_PAGE, count)
    return render_template('ads_list.html', pagination=posts, form=form)


if __name__ == "__main__":
    app.run(port=3000)
