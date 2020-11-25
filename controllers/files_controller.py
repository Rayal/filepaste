from werkzeug.utils import secure_filename

from filestore_interface import create_file_store_interface


def upload_file(request=None) -> (str, str):
    if "file" not in request.files:
        raise FileNotFoundError
    file = request.files["file"]
    if file.filename == "":
        raise NameError
    if file:
        filename = secure_filename(file.filename)
        with create_file_store_interface() as interface:
            file_id = interface.insert_file(filename, file.read())
            return file_id, filename


def download_file(file_id) -> (bytes, str):
    with create_file_store_interface() as interface:
        filename, file_data = interface.get_file(file_id)
        return bytes(file_data), filename


def delete_file(file_id) -> str:
    with create_file_store_interface() as interface:
        filename = interface.get_filename(file_id)
        interface.delete_file(file_id)
        return filename


def purge_files() -> None:
    with create_file_store_interface() as interface:
        interface.purge_files()
