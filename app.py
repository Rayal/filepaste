from io import BytesIO

from flask import (
    Flask,
    request,
    make_response,
    send_file,
    render_template,
)

from controllers.files_controller import upload_file, download_file, delete_file, purge_files
from filestore_interface import create_file_store_interface
from views.files_views import upload_file_view, upload_file_success, delete_file_success, purge_files_success

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 ** 3  # 1 GB


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/file", methods=["GET", "POST"])
def file():
    if request.method == "POST":
        file_id, filename = upload_file(request)
        return upload_file_success(
            filename=filename, download_location=f"/file/{file_id}"
        )
    return upload_file_view()


@app.route("/upload", methods=["GET", "POST"])
def upload():
    return file()


@app.route("/file/<file_id>")
def get_file(file_id):
    file_data, filename = download_file(file_id)
    return send_file(
        BytesIO(file_data), as_attachment=True, attachment_filename=filename
    )


@app.route("/download/<file_id>")
def download(file_id):
    return get_file(file_id)


@app.route("/file/<file_id>", methods=["DELETE"])
def delete(file_id):
    filename = delete_file(file_id)
    return delete_file_success(filename, "/file")


@app.route("/files", methods=["GET", "DELETE"])
def get_files():
    if request.method == "GET":
        with create_file_store_interface() as interface:
            files = interface.get_files()
            return render_template("files_list.html", files=files)
    else:
        purge_files()
        return purge_files_success("/files")


@app.route("/<path:path>")
def catch_all(path):
    response = make_response(f"Whoops! The endpoint {path} doesn't exist", 404)
    return response


if __name__ == "__main__":
    app.run()
