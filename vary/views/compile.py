import os

from flask import session, send_from_directory, request
from shutil import copyfile

from vary import app
from vary.model.generation.compile import generate_bbl
from vary.model.generation.generate import generate_pdf, generate_pdfs
from vary.model.files import create_temporary_copy, clear_directory


@app.route('/compile/<int:generations>', methods=["POST"])
def compile_pdfs(generations, reset=True):
    output = "vary/results"
    filename = session['main_file_name'].replace(".tex", "")  # main file name without extension
    source = os.path.join(app.config['UPLOAD_FOLDER'])  # The project is located in the "source" folder
    reset = request.form.get("reset") == 'true'

    generate_pdfs(filename, source, output, generations, reset)
    return send_from_directory("results", "result.csv")


@app.route('/build_pdf', methods=['GET', 'POST'])
def build_pdf():
    filename = session['main_file_name'].replace(".tex", "")
    if request.method == "GET":
        resp = send_from_directory("results", filename + ".pdf")
        resp.headers['Cache-Control'] = 'max-age=0, no-cache, must-revalidate'
        return resp

    config = request.form
    output = "vary/results"
    source = os.path.join(app.config['UPLOAD_FOLDER'])
    temp_path = create_temporary_copy(source)
    generate_bbl(os.path.join(temp_path, filename))

    generate_pdf(config, filename, temp_path)

    outpath = os.path.join(output, filename + ".pdf")
    if os.path.exists(outpath):
        os.remove(outpath)
    copyfile(
        os.path.join(temp_path, filename + ".pdf"),
        os.path.join(outpath)
    )
    clear_directory(os.path.dirname(temp_path))
    return '{"success":true}', 200, {'ContentType': 'application/json'}
