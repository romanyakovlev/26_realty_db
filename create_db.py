from main import db
import requests
from models import Apartment


url_path = "https://devman.org/assets/ads.json"


def get_json_data(url_path):
    json_data = requests.get(url_path).json()
    return json_data


if __name__ == "__main__":
    db.create_all()
    db.session.commit()
