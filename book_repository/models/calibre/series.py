from ...db import db
from .books_series_link import books_series_link

class Series(db.Model):
	__bind_key__ = "calibre"
	__tablename__ = "series"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(collation="NOCASE"), nullable=False, unique=True)
	sort = db.Column(db.String(collation="NOCASE"), nullable=True)

	books = db.relationship("Book", secondary=books_series_link, back_populates="series")
