"""
This file handles the plaintext data storage.
"""
from sqlalchemy import Column, Integer, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import relationship

from db_session import Base
from user import User


class PasteBin(Base):
    """
    The class PasteBin uses the SQLAlchemy Base system to define a SQL table which will contain all the plaintext data.
    The metadata will be used to maintain the database and ensure private data stays private.
    """
    __tablename__ = "pastebin"

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False)
    data = Column(Text, nullable=False)
    persistent = Column(Boolean, default=False)
    public = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship(User)

    @staticmethod
    def cleanup(hours=48) -> None:
        """
        This is used to maintain the database, removing non-persistent data that's older than the 'days' argument.
        :param hours: If the date and time in the 'created' column is older than the value of this, the respective row gets deleted.
        :return: None
        """

