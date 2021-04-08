import os
import conv2txt as conv
import textprocess as tps
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed' 
destFolder = "converted/"
dataFolder = "uploads/"
processedFolder = "processed/"

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
#           filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            conv.convertTOtxt(dataFolder, destFolder, filename)
 
            pre, ext = os.path.splitext(filename)
            filename = pre + '.txt'
            sentences = tps.sentProc(tps.sent_tokenize(tps.textProc(str(open(destFolder + filename, 'r').read())), language="russian"))

            with open(processedFolder + filename, 'w') as txtfile:
               for sent in sentences:
                 txtfile.write('%s\n' % sent)            

            return redirect(url_for('processed_file', filename=filename))
    return render_template('index.html')


if __name__=='__main__':
    app.run(debug=True)
