from main import db


class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    settlement = db.Column(db.String(500))
    under_construction = db.Column(db.Boolean)
    description = db.Column(db.String(500))
    price = db.Column(db.Integer)
    oblast_district = db.Column(db.String(500))
    living_area = db.Column(db.Integer, default=None)
    has_balcony = db.Column(db.Boolean)
    address = db.Column(db.String(500), default="")
    construction_year = db.Column(db.Integer, default=None)
    rooms_number = db.Column(db.Integer)
    premise_area = db.Column(db.Float)
    apartment_id = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.settlement
