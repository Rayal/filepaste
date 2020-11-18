"""
This file deals with creating connections to existing databases and handling their sessions.
"""
from os import environ

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()
_DB_ENGINE = None


def get_database_url() -> str:
    """
    Get the database URL from the 'DATABASE_URL' environment variable.
    :return: The database URL if the environment variable is set. An empty string if not.

    The string form of the URL is
    ``dialect[+driver]://user:password@host/dbname[?key=value..]``, where
    ``dialect`` is a database name such as ``mysql``, ``oracle``,
    ``postgresql``, etc., and ``driver`` the name of a DBAPI, such as
    ``psycopg2``, ``pyodbc``, ``cx_oracle``, etc.  Alternatively,
    the URL can be an instance of :class:`~sqlalchemy.engine.url.URL`.

    For example:
    "postgresql://username:password@localhost/database_name"
    """
    try:
        return environ["DATABASE_URL"]
    except KeyError:
        return ""


class DatabaseEngine:
    """
    A class to handle the database connection.
    """

    class DatabaseSession:
        """
        A class to handle the database session, with the help of a context manager.
        """

        def __init__(self, engine):
            """
            :param engine: The SQLAlchemy Engine object connected to the database.
            Expected use:
                engine = sqlalchemy.create_engine(database_url)
                # ... bind the engine to stuff ...
                DatabaseSession(engine)
            """
            self._engine = engine
            self._session = None

        def __enter__(self) -> Session:
            """
            Enter method for the context manager. Creates and returns a session
            :return: sqlalchemy.orm.Session
            """
            db_session = sessionmaker()
            db_session.bind = self._engine
            self._session = db_session()
            return self._session

        def __exit__(self, exc_type, exc_val, exc_tb) -> None:
            """
            Exit method for the context manager.
            :param exc_type: ...
            :param exc_val: ...
            :param exc_tb: ...
            :return: None
            """
            self._session.close()

    def __init__(self):
        """
        Creates a new database connection engine and binds it to the metadata object.
        :raises RuntimeError: If no database url is found in the environment variable 'DATABASE_URL'
        """
        database_url = get_database_url()
        if not database_url:
            raise RuntimeError("Whoops! No DB URL.")
        self._engine = create_engine(database_url)
        Base.metadata.bind = self._engine

    def get_session(self) -> DatabaseSession:
        """
        Returns a context manager enabling an active session to the database.
        :return: DatabaseEngine.DatabaseSession
        :raises OperationalError: If there is something wrong with the database URL,
            it will be raised here.
        """
        Base.metadata.create_all(self._engine)
        return DatabaseEngine.DatabaseSession(self._engine)


def get_engine() -> DatabaseEngine:
    """
    Return the currently active database engine.
    :return: The currently active database engine.

    The idea is to not have more than one engine running at a time.
    """
    global _DB_ENGINE
    if not _DB_ENGINE:
        _DB_ENGINE = DatabaseEngine()
    return _DB_ENGINE
