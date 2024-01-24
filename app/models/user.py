from dataclasses import asdict, dataclass
from enum import Enum

from .abstract_model import AbstractModel


class IdentityProvider(Enum):
    GOOGLE = "google"
    MICROSOFT = "microsoft"


@dataclass
class User(AbstractModel):
    username: str
    salt: str
    password_hash: str
    _id: str = None


@dataclass
class UserProfile:
    email: str
    name: str
    picture_url: str
    first_name: str
    last_name: str
    idp: IdentityProvider

    def as_json(self):
        data = asdict(self)
        data["idp"] = self.idp.value
        return data


@dataclass
class AuthenticatedUserProfile(UserProfile):
    id: str

    @classmethod
    def from_user_profile(cls, user_profile: UserProfile, user_id: str):
        return cls(id=user_id, **asdict(user_profile))
