from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foo.db'
app.secret_key = 'super secret key'
db = SQLAlchemy(app)
