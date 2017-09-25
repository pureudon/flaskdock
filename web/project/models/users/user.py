import uuid
from project.common.database import Database
from project.common.utils import Utils
import project.models.users.errors as UserErrors
import project.models.users.constants as UserConstants
from project.models.alerts.alert import Alert

class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "User {}".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        This is method verfies that and email/password combo (as sent by the site forms) is valud or not.
        :param email: The user's email
        :param password: A sha512 hashed password
        :return: Ture if valid, False otherwise
        """

        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})  # Password in sha512 -> pbkdf2_sha512
        if user_data is None:
            raise UserErrors.UserNotExistsError("Your user does not exist.")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Your password was wrong.")

        return True


    @staticmethod
    def register_user(email, password):
        """
        This method registers a user using email and password.
        The password already comes hashed as sha-512.
        :param email: user's eamil (might be invalid)
        :param password: sha512-hashed password
        :return: True if registered successfully, or False otherwise (exceptiopns can also be raised)
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})

        if user_data is not None:
            # Tell user they are already registered
            raise UserErrors.UserAlreadyRegisteredError("The email you used to register already exists.")
        if not Utils.email_is_valid(email):
            # Tell user that their email is not constructed properly.
            raise UserErrors.InvalidEmailError("The email does not have the format.")

        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert("users", self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {"email": email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)