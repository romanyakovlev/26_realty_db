from models import Apartment
import random
import json
from app import db

with open('data.json') as data_file:
    json_data = json.load(data_file)


if __name__ == "__main__":
    for apartment_dict in json_data:
        db.session.add(Apartment(**apartment_dict))
    db.session.commit()
    db.session.close()
