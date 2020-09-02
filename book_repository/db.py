from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import BindMetaMixin, Model
from sqlalchemy import event
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.pool import Pool


class NoNameMeta(BindMetaMixin, DeclarativeMeta):
	pass


db = SQLAlchemy(
	model_class=declarative_base(
		cls=Model,
		metaclass=NoNameMeta,
		name="Model"
	)
)
