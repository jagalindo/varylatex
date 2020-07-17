import os
import json
import re

from flask import request, redirect, url_for, render_template, session

from vary import app


@app.route('/selectfile', methods=["GET", "POST"])
def selectfile():
    if request.method == "POST":
        session['main_file_name'] = request.form.get('filename')
        return redirect(url_for('results'))
    else:
        name = session['project_name']
        return render_template('selectfile.html', name=name)


@app.route('/filenames')
def get_filenames():
    """
    Gets the potential main tex file names based on the content of the source folder and
    the fact that it contains or not a \documentclass{} declaration
    """
    filenames = []
    dc_pattern = re.compile(r"^[^%]*\\documentclass\{[^}]*\}")
    texfile_pattern = re.compile(r".*\.tex")
    for root, _, files in os.walk("vary/source"):
        for filename in files:
            if texfile_pattern.match(filename):
                path = os.path.join(root, filename)
                with open(path) as file:
                    data = file.read()
                    if any(li for li in data.splitlines() if dc_pattern.match(li)):
                        filenames.append(os.path.relpath(path, "vary/source"))

    return json.dumps(filenames)
