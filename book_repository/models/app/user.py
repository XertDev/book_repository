import enum
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from ...db import db


class UserType(enum.Enum):
	ADMIN = "ADMIN"
	NORMAL = "NORMAL"


class User(db.Model, UserMixin):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(128), nullable=False, unique=True)
	email = db.Column(db.String(256), nullable=False, unique=True)
	type = db.Column(db.Enum(UserType), nullable=False)
	password_hash = db.Column(db.String(128), nullable=False)

	creation_time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now)

	push_emails = db.relationship("PushEmail", cascade="all, delete", back_populates="user")
	book_permissions = db.relationship("BookPermission", cascade="all, delete", back_populates="user")

	def set_password(self, password: str) -> None:
		self.password_hash = generate_password_hash(password)

	def check_password(self, password: str) -> bool:
		return check_password_hash(self.password_hash, password)

	def get_id(self):
		return self.id

	def is_admin(self):
		return self.type == UserType.ADMIN
