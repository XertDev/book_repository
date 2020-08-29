from datetime import datetime

from ...db import db


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
