from io import BytesIO

from flask import (
    Flask,
    request,
    redirect,
    flash,
    make_response,
    jsonify,
    send_file,
    render_template,
)
from werkzeug.utils import secure_filename

from filestore_interface import create_file_store_interface


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 ** 3  # 1 GB


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/file", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file found")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No file found")
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            with create_file_store_interface() as interface:
                file_id = interface.insert_file(filename, file.read())
                response = make_response(jsonify({"fileId": file_id}), 201)
            response.headers["Content-Type"] = "application/json"
            return response

    return """
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        """


@app.route("/file/<file_id>")
def get_file(file_id):
    with create_file_store_interface() as interface:
        filename, file_data = interface.get_file(file_id)
        return send_file(
            BytesIO(bytes(file_data)), as_attachment=True, attachment_filename=filename
        )


@app.route("/download/<file_id>")
def download(file_id):
    return get_file(file_id)


@app.route("/file/<file_id>", methods=["DELETE"])
def delete(file_id):
    with create_file_store_interface() as interface:
        interface.delete_file(file_id)
    return make_response()


@app.route("/files", methods=["GET", "DELETE"])
def get_files():
    if request.method == "GET":
        with create_file_store_interface() as interface:
            files = interface.get_files()
            return render_template("files_list.html", files=files)
    else:
        with create_file_store_interface() as interface:
            interface.purge_files()


if __name__ == "__main__":
    app.run()
