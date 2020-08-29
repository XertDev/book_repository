from ...db import db
from .books_publishers_link import books_publishers_link


class Publisher(db.Model):
	__bind_key__ = "calibre"
	__tablename__ = "publishers"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(collation="NOCASE"), nullable=False, unique=True)
	sort = db.Column(db.String(collation="NOCASE"), nullable=True)

	books = db.relationship("Book", secondary=books_publishers_link, back_populates="publishers")
