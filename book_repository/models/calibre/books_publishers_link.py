from ...db import db


books_publishers_link = db.Table(
	"books_publishers_link",
	db.Column("id", db.Integer, primary_key=True),
	db.Column("book", db.Integer, db.ForeignKey("books.id"), nullable=False),
	db.Column("publisher", db.Integer, db.ForeignKey("publishers.id"), nullable=False),
	info={"bind_key": "calibre"}
)
