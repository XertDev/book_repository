from ...db import db


books_tags_link = db.Table(
	"books_tags_link",
	db.Column("id", db.Integer, primary_key=True),
	db.Column("book", db.Integer, db.ForeignKey("books.id"), nullable=False),
	db.Column("tag", db.Integer, db.ForeignKey("tags.id"), nullable=False),
	info={"bind_key": "calibre"}
)
