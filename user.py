"""
This file handles user data on the SQL database
"""

from sqlalchemy import Column, Integer, Boolean, Text
from werkzeug.security import generate_password_hash, check_password_hash

from db_session import Base


class User(Base):
    """
    The class User uses the SQLAlchemy Base system to define a SQL table.
    In addition it acts as an interface for the relevant row changes.
    """

    __tablename__ = "users"

    _id = Column(Integer, primary_key=True, name="id")
    _username = Column(Text, nullable=False, unique=True, name="username")
    _password = Column(Text, nullable=False, name="password")
    _admin = Column(Boolean, default=False, name="admin")

    def __init__(self, username: str, password: str, admin=False):
        self._username = username
        self.set_password(password)
        self._admin = admin

    def set_password(self, password: str) -> None:
        """
        Changes the password for a given user.
        :param password: The new password in plaintext.
        :return: None

        The password is hashed and the hash stored in the database.
        """
        self._password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Checks to see if the password in the argument matches the one stored in the database.
        :param password: The password to check, in plaintext.
        :return: True if the password matches.

        The plaintext password is hashed and compared to the hashed password stored in the database.
        """
        if password and self._password:
            return check_password_hash(self._password, password)
        return False

    @staticmethod
    def create_table_if_needed():
        Base.metadata.bind
