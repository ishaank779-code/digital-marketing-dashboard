from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # MySQL connection
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'mysql+pymysql://dashboard:dashboard123@localhost/marketing_dashboard'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'digital-marketing-dashboard-secret-key-2026'

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    return app
