from app import db
from models import Apartment
from json_file import catalog


if __name__ == "__main__":
    db.create_all()
    db.session.commit()
