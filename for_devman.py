json_data = get_json_data(url_path)

def make_old_ads_unactive(db):
    active_ads_arr = db.session.query(Apartment).filter(Apartment.active == True).all()
    for apartment_advert in active_ads_arr:
        apartment_advert.active = False

def insert_new_ads_into_db(db, json_data):
    for apartment_advert in json_data:
        db.session.add(Apartment(**apartment_advert))

try:
    make_old_ads_unactive(db)
    insert_new_ads_into_db(db, json_data)
    db.session.commit()
except sqlalchemy.exc.OperationalError as e:
    print(e)
    db.session.rollback()
except sqlalchemy.exc.TimeoutError as e:
    print(e)
    db.sessio.rollback()
db.session.close()
