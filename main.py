import os
import conv2txt as conv
import textprocess as tps
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory

UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted' 
destFolder = "converted/"
dataFolder = "uploads/"


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONVERTED_FOLDER'] = CONVERTED_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/converted/<filename>')
def converted_file(filename):
    return send_from_directory(app.config['CONVERTED_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
#           filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            conv.convertTOtxt(dataFolder, destFolder, filename)
            
            x = filename.split('.')
            filename = str(x[0]) + '.txt'

            return redirect(url_for('converted_file', filename=filename))
    return render_template('index.html')


if __name__=='__main__':
    app.run(debug=True)
