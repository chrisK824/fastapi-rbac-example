from enum import Enum
from typing import Union, Type
import re
from dataclasses import dataclass


@dataclass(init=False, eq=False)
class Permission:
    """
    Base class for permissions.
    Allows for easy comparison of different notations.
    E.g. Permission('CREATE') == 'CREATE'.
    """
    permission_type: str

    def __init__(self, permission_type: str):
        self.permission_type = str(permission_type)

    @property
    def full_name(self) -> str:
        return str(self.permission_type)

    def __str__(self):
        return self.full_name

    def __eq__(self, other):
        if (
            isinstance(other, str)
            or isinstance(other, Permission)
            or issubclass(other, Permission)
        ):
            return str(self.full_name) == str(other)
        return False

    def __hash__(self):
        return hash(self.full_name)


class PermissionType(str, Enum):
    """
    Enum for the different types of default
    permissions that can be applied to a model.
    """
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

    def __str__(self):
        return f"{self.value}"


@dataclass(eq=False)
class ModelPermission(Permission):
    """
    A higher-level of abstraction for the Permission class.
    A ModelPermission with permission_type=CREATE and permission_model=Example
    is equivalent to a Permission with permission_type=`Example_CREATE`.
    """
    permission_type: Union[PermissionType, str]
    permission_model: Type

    @property
    def full_name(self) -> str:
        model_name = re.sub(
            r"(?<!^)(?=[A-Z])", "_", self.permission_model.__name__
        ).upper()
        return f"{model_name}_{self.permission_type.__str__().upper()}"

    def __str__(self):
        return self.full_name


class ModelDefaultPermissions:
    """
    Class that provides a set of default permissions used by a model.
    It is used by the ModelPermissions class.
    """

    def __init__(self, model):
        self.CREATE = ModelPermission(
            permission_type=PermissionType.CREATE, permission_model=model
        )
        self.READ = ModelPermission(
            permission_type=PermissionType.READ, permission_model=model
        )
        self.UPDATE = ModelPermission(
            permission_type=PermissionType.UPDATE, permission_model=model
        )
        self.DELETE = ModelPermission(
            permission_type=PermissionType.DELETE, permission_model=model
        )


class ModelPermissions:
    """
    Provides the default set of permissions
    under the `permissions` attribute.
    """

    @classmethod
    @property
    def permissions(cls) -> ModelDefaultPermissions: # noqa
        return ModelDefaultPermissions(cls)