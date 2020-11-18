from os import environ
from uuid import uuid4
import psycopg2 as pg  # type: ignore


def get_database_url() -> str:
    return environ["DATABASE_URL"]


def get_database_password() -> str:
    try:
        return environ["DATABASE_PASSWORD"]
    except KeyError:
        return ""


class FileStoreInterface:
    def _create_connection(self, **kwargs) -> None:
        self._connection = pg.connect(self._database_url, sslmode="require", **kwargs)
        self._cursor = self._connection.cursor()

    def __init__(self, **kwargs):
        self._connection = None
        self._cursor = None
        self._database_url = get_database_url()
        self._create_connection(**kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(exc_type, exc_val, exc_tb)
        self._cursor.close()
        self._connection.close()

    def insert_file(self, filename: str, file_data: bytes) -> str:
        uuid = str(uuid4())
        query = "INSERT INTO paste (id, filename, file_data) VALUES (%(id)s, %(str)s, %(bytes)s);"
        mapping = {"id": uuid, "str": filename, "bytes": file_data}
        self._cursor.execute(query, mapping)
        self._connection.commit()
        return uuid

    def get_file(self, file_id: str) -> (str, memoryview):
        if file_id:
            query = "SELECT filename, file_data FROM paste where id = %s;"
            self._cursor.execute(query, (file_id,))
            return self._cursor.fetchone()
        raise FileNotFoundError(file_id)

    def get_files(self) -> list:
        query = "SELECT id, filename from paste;"
        self._cursor.execute(query)
        return self._cursor.fetchall()


def create_file_store_interface() -> FileStoreInterface:
    password = get_database_password()
    if password:
        return FileStoreInterface(password=password)
    return FileStoreInterface()
