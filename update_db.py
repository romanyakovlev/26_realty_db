
from models import Apartment
import requests
from main import db
import sqlalchemy


url_path = "https://devman.org/assets/ads.json"


def get_json_data(url_path):
    json_data = requests.get(url_path).json()
    return json_data


def make_old_ads_unactive(db):
    active_ads_arr = db.session.query(Apartment).filter(Apartment.active == True).all()
    for apartment_advert in active_ads_arr:
        apartment_advert.active = False


def insert_new_ads_into_db(db, json_data):
    for apartment_advert in json_data:
        db.session.add(Apartment(**apartment_advert))


if __name__ == "__main__":
    json_data = get_json_data(url_path)
    try:
        make_old_ads_unactive(db)
        insert_new_ads_into_db(db, json_data)
        db.session.commit()
    except sqlalchemy.orm.exc.FlushError:
        print('Now you are trying to insert into db advert with id which already exist.Db changes is rolled back.')
        db.session.rollback()
    except sqlalchemy.exc.TimeoutError:
        print('Connection pool times out on getting a connection')
        db.sessio.rollback()
    db.session.close()
