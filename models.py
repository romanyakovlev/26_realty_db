from main import db
from datetime import date

year_limit = 2
string_length = 500


class Apartment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    settlement = db.Column(db.String(string_length))
    under_construction = db.Column(db.Boolean)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, index=True)
    oblast_district = db.Column(db.String(string_length), index=True)
    living_area = db.Column(db.Integer, default=None)
    has_balcony = db.Column(db.Boolean)
    address = db.Column(db.String(string_length), default="")
    construction_year = db.Column(db.Integer, default=None)
    rooms_number = db.Column(db.Integer)
    premise_area = db.Column(db.Float)
    apartment_id = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True, index=True)
    new_building = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.settlement

    def __init__(self, **kwargs):
        super(Apartment, self).__init__(**kwargs)
        current_year = date.today().year
        if self.under_construction is True:
            self.new_building = True
        if isinstance(self.construction_year, int):
            if current_year - self.construction_year <= year_limit:
                self.new_building = True
