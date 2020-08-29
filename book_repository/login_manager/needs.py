from collections import namedtuple
from functools import partial

from flask_principal import RoleNeed

admin_user = RoleNeed("admin")
normal_user = RoleNeed("normal")
