import base64
import hashlib
import uuid

from pymongo.collection import Collection

from ..exceptions import NotFoundException
from ..models.user import AuthenticatedUserProfile, User, UserProfile
from .db_service import DbService


class UserService(DbService):
    def register(self, username: str, password: str):
        salt = base64.urlsafe_b64encode(uuid.uuid4().bytes)
        sha = hashlib.sha512()
        sha.update(password.encode() + salt)
        password_hash = sha.hexdigest()
        user = User(username=username, salt=salt.decode(), password_hash=password_hash)

        with self.get_database() as db:
            users_coll: Collection = db["users"]
            users_coll.insert_one(user.as_json())

    def login(self, username: str, password: str):
        with self.get_database() as db:
            users_coll: Collection = db["users"]
            user_dict = users_coll.find_one({"username": username})

        if not user_dict:
            raise NotFoundException("Username or password do not match")

        user = User(**user_dict)
        sha = hashlib.sha512()
        sha.update(password.encode() + user.salt.encode())
        password_hash = sha.hexdigest()
        if password_hash != user.password_hash:
            raise NotFoundException("Username or password do not match")

    def login_with_idp(self, user: UserProfile) -> AuthenticatedUserProfile:
        with self.get_database() as db:
            users_coll: Collection = db["users"]
            user_dict = users_coll.find_one({"email": user.email, "idp": user.idp.value})
            if user_dict:
                user_id = str(user_dict["_id"])
                return AuthenticatedUserProfile.from_user_profile(user, user_id)

            user_dict = user.as_json()
            resp = users_coll.insert_one(user_dict)
            return AuthenticatedUserProfile.from_user_profile(user, str(resp.inserted_id))
