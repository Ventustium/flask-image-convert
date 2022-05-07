#Use this file if you want to save the image that already converted
import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from PIL import Image

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', error=' .jpg, .jpeg dan .png only')
    
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('index.html', error='No File Part')

        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return render_template('index.html', error='No Image Selected')

        if allowed_file(file.filename) == False:
            return render_template('index.html', error='Select .jpg, .jpeg dan .png only')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            splitName = os.path.splitext(filename)
            formatfilename = splitName[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "original/", filename))
            convertedname = splitName[0]+"-gray"+formatfilename
            img = Image.open('static/original/'+filename).convert('L')
            img.save('static/converted/'+convertedname)
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], "original/", filename)
            full_filenameConvert = os.path.join(app.config['UPLOAD_FOLDER'], "converted/", convertedname)

            return render_template('result.html', image=full_filename, imageConvert=full_filenameConvert)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run(host='0.0.0.0', port=9018)