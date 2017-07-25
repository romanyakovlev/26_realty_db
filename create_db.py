from main import db


if __name__ == "__main__":
    db.create_all()
    db.session.commit()
    db.session.close()
