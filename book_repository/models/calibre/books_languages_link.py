from ...db import db


books_languages_link = db.Table(
	"books_languages_link",
	db.Column("id", db.Integer, primary_key=True),
	db.Column("book", db.Integer, db.ForeignKey("books.id"), nullable=False),
	db.Column("lang_code", db.Integer, db.ForeignKey("languages.id"), nullable=False),
	db.Column("item_order", db.Integer, nullable=False, default=0),
	info={"bind_key": "calibre"}
)
