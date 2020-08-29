import enum

from book_repository.db import db


class BookPermissionType(enum.Enum):
	EDIT = "EDIT"
	VIEW = "VIEW"


class BookPermission(db.Model):
	__tablename__ = "book_permission"

	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
	book_id = db.Column(db.Integer, db.ForeignKey("books.id"), primary_key=True)

	type = db.Column(db.Enum(BookPermissionType), nullable=False)

	user = db.relationship("User", back_populates="book_permissions")
	book = db.relationship("Book", lazy="select", primaryjoin="Book.id == BookPermission.book_id", uselist=False)
