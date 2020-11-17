from io import BytesIO

from flask import Flask, request, redirect, flash, make_response, jsonify, send_file, render_template
from werkzeug.utils import secure_filename

from filestore_interface import create_file_store_interface

DISALLOWED_EXTENSIONS = {'html', 'php'}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 ** 3  # 1 GB


def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() not in DISALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file found")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash("No file found")
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            response = make_response(jsonify({
                    "message": "Whoops!"
                }), 503)
            with create_file_store_interface() as interface:
                file_id = interface.insert_file(filename, file.read())
                response = make_response(jsonify({
                    "fileId": file_id
                }), 201)
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


@app.route("/download/<file_id>")
def download(file_id):
    with create_file_store_interface() as interface:
        filename, file_data = interface.get_file(file_id)
        return send_file(
            BytesIO(bytes(file_data)),
            as_attachment=True,
            attachment_filename=filename)


@app.route("/files")
def get_files():
    with create_file_store_interface() as interface:
        files = interface.get_files()
        return render_template("files_list.html", files=files)


if __name__ == '__main__':
    app.run()
