from app import db


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean)
    initial_date = db.Column(db.Date, nullable=False)
    last_date = db.Column(db.Date)
    user_order = db.Column(db.Integer, nullable=False)
    last_update = db.Column(db.Date, nullable=False)
    deleted = db.Column(db.Date, nullable=True)
