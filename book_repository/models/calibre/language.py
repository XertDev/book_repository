from ...db import db
from .books_languages_link import books_languages_link


class Language(db.Model):
	__bind_key__ = "calibre"
	__tablename__ = "languages"

	id = db.Column(db.Integer, primary_key=True)
	lang_code = db.Column(db.String(collation="NOCASE"), nullable=False, unique=True)

	books = db.relationship("Book", secondary=books_languages_link)
