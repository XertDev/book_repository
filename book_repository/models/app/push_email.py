from datetime import datetime

from ...db import db


class PushEmail(db.Model):
	__tablename__ = "push_emails"

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(256))
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
	name = db.Column(db.String, nullable=False, unique=True)

	creation_time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now)

	user = db.relationship("User", uselist=False, back_populates="push_emails")
