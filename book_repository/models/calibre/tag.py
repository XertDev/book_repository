from ...db import db
from .books_tags_link import books_tags_link


class Tag(db.Model):
	__bind_key__ = "calibre"
	__tablename__ = "tags"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(collation="NOCASE"), nullable=False, unique=True)

	books = db.relationship("Book", secondary=books_tags_link, back_populates="tags")
