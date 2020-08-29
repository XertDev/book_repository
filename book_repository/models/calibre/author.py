from ...db import  db
from .books_authors_link import books_authors_link

class Author(db.Model):
	__bind_key__ = "calibre"
	__tablename__ = "authors"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(collation="NOCASE"), nullable=False, unique=True)
	sort = db.Column(db.String(collation="NOCASE"), nullable=True)
	link = db.Column(db.String, nullable=False, default="")

	books = db.relationship("Book", secondary=books_authors_link, back_populates="authors")
