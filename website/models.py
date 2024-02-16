from datetime import datetime
from website import db

class WeeklyData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10), nullable=False)
    total_items = db.Column(db.Float, nullable=False)
    most_popular_item = db.Column(db.String(10), nullable=False)
    least_popular_item = db.Column(db.String(10), nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    max_cost = db.Column(db.Float, nullable=False)
    min_cost = db.Column(db.Float, nullable=False)
    average_cost = db.Column(db.Float, nullable=False)
    least_popular_payment = db.Column(db.String(10), nullable=False)
    most_popular_staff = db.Column(db.String(10), nullable=False)
    # complete = db.Column(db.Boolean, default = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_edited = db.Column(db.DateTime, onupdate=datetime.utcnow)
    # date_completed = db.Column(db.DateTime, default=None)
    # date_deleted = db.Column(db.DateTime, default=datetime.utcnow)