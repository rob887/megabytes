from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .models import db
    db.init_app(app)

    from .views import my_view
    app.register_blueprint(my_view)

    with app.app_context():
        db.create_all()

    return app