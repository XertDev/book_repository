from ...db import db


books_series_link = db.Table(
	"books_series_link",
	db.Column("id", db.Integer, primary_key=True),
	db.Column("book", db.Integer, db.ForeignKey("books.id"), nullable=False),
	db.Column("series", db.Integer, db.ForeignKey("series.id"), nullable=False),
	info={"bind_key": "calibre"}
)
