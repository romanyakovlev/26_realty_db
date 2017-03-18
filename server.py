from flask import Flask, render_template, request, url_for
from app import app
from models import Apartment
from math import ceil

class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


apartments_array = []
for apartment_dict in Apartment.query.all():
    apartments_array.append({
            "settlement": apartment_dict.settlement,
            "under_construction": apartment_dict.under_construction,
            "description": apartment_dict.description,
            "price": apartment_dict.price,
            "oblast_district": apartment_dict.oblast_district,
            "living_area": apartment_dict.living_area,
            "has_balcony": apartment_dict.has_balcony,
            "address": apartment_dict.address,
            "construction_year": apartment_dict.construction_year,
            "rooms_number": apartment_dict.rooms_number,
            "premise_area": apartment_dict.premise_area,
    })


POSTS_PER_PAGE = 3
@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def homepage(page):
  count = Apartment.query.count()
  posts = Apartment.query.paginate(page,POSTS_PER_PAGE, count).items

  pagination = Pagination(page, POSTS_PER_PAGE, count)
  return render_template('ads_list.html',
                            ads=apartments_array,
                            pagination=pagination)



if __name__ == "__main__":
    app.run(port=3000)
