from enum import Enum
from permissions.models_permissions import *


class Role(str, Enum):
    ADMINISTRATOR = "ADMINISTRATOR"
    USER = "USER"

    @classmethod
    def get_roles(cls):
        values = []
        for member in cls:
            values.append(f"{member.value}")
        return values


ROLE_PERMISSIONS = {
    Role.ADMINISTRATOR: [
        [
            Users.permissions.CREATE,
            Users.permissions.READ,
            Users.permissions.UPDATE,
            Users.permissions.DELETE
        ],
        [
            Items.permissions.CREATE,
            Items.permissions.READ,
            Items.permissions.UPDATE,
            Items.permissions.DELETE
        ]
    ],
    Role.USER: [
        [
            Items.permissions.CREATE,
            Items.permissions.READ,
            Items.permissions.UPDATE
        ]
    ]
}


def get_role_permissions(role: Role):
    permissions = set()
    for permissions_group in ROLE_PERMISSIONS[role]:
        for permission in permissions_group:
            permissions.add(str(permission))
    return list(permissions)
