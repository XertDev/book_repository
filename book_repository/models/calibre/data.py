from ...db import db


class Data(db.Model):
	__bind_key__ = "calibre"
	__tablename__ = "data"

	id = db.Column(db.Integer, primary_key=True)
	book = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False, unique=True)
	format = db.Column(db.String(collation="NOCASE"), nullable=False)
	uncompressed_size = db.Column(db.Integer, nullable=False)
	name = db.Column(db.String, nullable=False)

	linked_book = db.relationship("Book", uselist=False, back_populates="data")
