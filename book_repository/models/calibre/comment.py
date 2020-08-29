from ...db import db


class Comment(db.Model):
	__bind_key__ = "calibre"
	__tablename__ = "comments"

	id = db.Column(db.Integer, primary_key=True)
	book = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False, unique=True)
	text = db.Column(db.String(collation="NOCASE"), nullable=False)

	commented_book = db.relationship("Book", uselist=False, back_populates="comment")
