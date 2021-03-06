from flask_wtf import Form
from wtforms import HiddenField, SubmitField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email


class AddPushEmailForm(Form):
	name = StringField("Name", [DataRequired()])
	email = EmailField("Email", [DataRequired(), Email()])
	add = SubmitField('add')


class DelPushEmailForm(Form):
	email_id = HiddenField("Email id", [DataRequired()])
	delete = SubmitField('delete')
