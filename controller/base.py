import os
import re

from flask import (Blueprint, flash, render_template, send_from_directory, request, send_file, Response)

from controller.image_processor.constants import BASE_DIR
from controller.image_processor.entry import input_file, upload_video_file

STORAGE_DIR = os.path.join(BASE_DIR, 'storage', 'video')

base = Blueprint('base',__name__)

# Serve files directly through a route (more control)
@base.route('/video/<folder>/<filename>')
def serve_storage_file(folder, filename):
    return send_from_directory(os.path.join(STORAGE_DIR, folder), filename, as_attachment= True)


@base.route("/ping")
def ping_test():
    input_file('test1.mp4')
    return render_template('index.html')

@base.route('/', methods=['POST', 'GET'])
def convert_to_cartoon():
    folder = ''
    filename = ''
    if request.method == 'POST':
        filename = request.form.get('filename')
        file = request.files.get('file')
        
        if filename == '':
            flash("filename is required!", 400)
            
        if not file:
            flash("No file uploaded!", 400)
            
        filename_with_extension = upload_video_file(filename, file)
        input_file(filename_with_extension)
        
        return render_template('index.html', folder=filename, filename=filename_with_extension)
    else:
        return render_template('index.html', folder=folder, filename=filename)

@base.route('/recents', methods=['GET'])
@base.route('/recents/<folder>/<filename>', methods=['GET'])
def recent_conversions(folder='', filename=''):
    dirs = os.listdir(STORAGE_DIR)
    print(dirs)
    return render_template('recents.html', folder=folder, filename=filename, directories=dirs)

