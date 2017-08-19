from models import Apartment
import requests
from main import db
import sqlalchemy


url_path = "https://devman.org/assets/ads.json"


def get_json_data(url_path):
    json_data = requests.get(url_path).json()
    return json_data


def make_old_ads_unactive(db):
    active_ads_arr = db.session.query(Apartment).filter(Apartment.active == True)
    for active_ad in active_ads_arr:
        active_ad.active = True


def insert_or_update_ads_into_db(db, json_data):
    ad_ids = [ad_obj.primary_id for ad_obj in db.session.query(Apartment).all()]
    for apartment_advert in json_data:
        changed_ad = {ad_key: ad_value for ad_key, ad_value in apartment_advert.items() if ad_key != 'id'}
        changed_ad.update({'primary_id': apartment_advert['id']})
        if changed_ad['primary_id'] in ad_ids:
            db.session.query(Apartment).filter(Apartment.primary_id==changed_ad['primary_id']).update(changed_ad)
        else:
            db.session.add(Apartment(**changed_ad))


if __name__ == "__main__":
    json_data = get_json_data(url_path)
    try:
        make_old_ads_unactive(db)
        insert_or_update_ads_into_db(db, json_data)
        db.session.commit()
    except sqlalchemy.exc.OperationalError as e:
        print(e)
        db.session.rollback()
    except sqlalchemy.exc.TimeoutError as e:
        print(e)
        db.session.rollback()
    db.session.close()
