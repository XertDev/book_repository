from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
	"""Login to user account"""

	username = StringField(
		"Username",
		[
			DataRequired()
		]
	)

	password = PasswordField(
		"Password",
		[
			DataRequired("Please enter a password")
		]
	)
