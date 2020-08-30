from datetime import datetime

from ...db import db
from .books_authors_link import books_authors_link
from .books_languages_link import books_languages_link
from .books_series_link import books_series_link
from .books_tags_link import books_tags_link
from .books_publishers_link import books_publishers_link


class Book(db.Model):
	__bind_key__ = "calibre"
	__tablename__ = "books"

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(collation="NOCASE"), nullable=False, default="Unknown")
	sort = db.Column(db.String(collation="NOCASE"), nullable=True)
	timestamp = db.Column(db.TIMESTAMP, nullable=True, default=datetime.now)
	pubdate = db.Column(db.TIMESTAMP, nullable=True, default=datetime.now)
	series_index = db.Column(db.REAL, nullable=False, default=1.0)
	author_sort = db.Column(db.String(collation="NOCASE"), nullable=True)
	isbn = db.Column(db.String(collation="NOCASE"), nullable=True, default="")
	lccn = db.Column(db.String(collation="NOCASE"), nullable=True, default="")
	path = db.Column(db.String, nullable=False, default="")
	flags = db.Column(db.Integer, nullable=False, default=1)
	uuid = db.Column(db.String, nullable=True)
	has_cover = db.Column(db.Boolean, nullable=False, default=0)
	last_modified = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now)

	authors = db.relationship("Author", secondary=books_authors_link, back_populates="books")
	languages = db.relationship(
		"Language", secondary=books_languages_link, back_populates="books",
		order_by="books_languages_link.c.item_order"
	)
	series = db.relationship("Series", secondary=books_series_link, back_populates="books")
	tags = db.relationship("Tag", secondary=books_tags_link, back_populates="books")
	publishers = db.relationship("Publisher", secondary=books_publishers_link, back_populates="books")
	comment = db.relationship("Comment", back_populates="commented_book", uselist=False)
	data = db.relationship("Data", back_populates="linked_book")
