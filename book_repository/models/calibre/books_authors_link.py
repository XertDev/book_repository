from ...db import db


books_authors_link = db.Table(
	"books_authors_link",
	db.Column("id", db.Integer, primary_key=True),
	db.Column("book", db.Integer, db.ForeignKey("books.id"), nullable=False),
	db.Column("author", db.Integer, db.ForeignKey("authors.id"), nullable=False),
	info={"bind_key": "calibre"}
)
