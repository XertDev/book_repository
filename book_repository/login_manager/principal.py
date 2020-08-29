from flask_login import current_user
from flask_principal import Principal, identity_loaded, UserNeed

from ..models.app.user import UserType
from . import needs

principal = Principal()

role_map = {
	UserType.ADMIN: needs.admin_user,
	UserType.NORMAL: needs.normal_user
}


@identity_loaded.connect
def on_identity_loaded(sender, identity):
	identity.user = current_user

	if hasattr(current_user, "id"):
		identity.provides.add(UserNeed(current_user.id))

	if hasattr(current_user, "type"):
		if current_user.type in role_map:
			identity.provides.add(role_map[current_user.type])
