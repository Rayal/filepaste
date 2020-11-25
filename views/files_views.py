from flask import render_template


def upload_file_view() -> str:
    return render_template("upload_file.html")


def upload_file_success(filename: str, download_location: str) -> str:
    return render_template(
        "upload_file_success.html",
        filename=filename,
        download_location=download_location,
    )


def delete_file_success(filename: str, upload_url: str) -> str:
    return render_template(
        "delete_file_success.html", filename=filename, upload_url=upload_url
    )


def purge_files_success(upload_url: str) -> str:
    return render_template("purge_files_success.html", upload_url=upload_url)


def file_list_view(files: list) -> str:
    return render_template("files_list.html", files=files)
