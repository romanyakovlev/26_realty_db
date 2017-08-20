from main import db
import requests
from models import Apartment


if __name__ == "__main__":
	db.create_all()
	db.session.commit()
