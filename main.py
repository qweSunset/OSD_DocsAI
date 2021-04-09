import os
import numpy as np
import conv2txt as conv
import textprocess as tps
import tokenizer as tkr
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

def logging(textLog):
    f = open('log/mainErrlog.txt','a')
    f.write(textLog+'\n')
    f.close()

def procLog(textLog):
    f = open('log/processLog.txt','a')
    f.write(textLog+'\n')
    f.close()

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
            try:
               conv.convertTOtxt(dataFolder, destFolder, filename)
            except Exception:
                conv.logging('Something goes wrong with convertation' + filename)
            pre, ext = os.path.splitext(filename)
            filename = pre + '.txt'
            if os.path.exists(destFolder + filename):
               try:
                 sentences = tps.sentProc(tps.sent_tokenize(tps.textProc(str(open(destFolder + filename, 'r').read())), language="russian"))
               except Exception:
                 logging('Something goes wrong on sent tokenizer with' + filename)
            with open(processedFolder + filename, 'w') as txtfile:
               for sent in sentences:
                 txtfile.write('%s\n' % sent)
            if os.path.exists(processedFolder + filename):
               set_words = tps.getWords(sentences)
               procLog('set_words: \n' + str(set_words[0]))
               tokenized = tkr.tokenWords(set_words)
               X_word = tokenized[0]
          #     X_word = np.asarray(X_word).astype(np.int32)
               procLog('X_word: \n' + str(X_word.shape))
               unkWords = tokenized[1]
               X_char = tkr.tokenChars(set_words)
          #     X_char = np.asarray(X_char).astype(np.int64)
               procLog('X_char: \n' + str(X_char.shape))
               test_pred = tkr.model.predict([X_word, X_char], verbose=0)
            try:
               jsonString = tkr.getJson(test_pred, X_word, unkWords)
               conv.logging(jsonString)
            except Exception:
               logging('Something goes wrong on pred model with  ' + filename)
            with open(processedFolder + filename, 'w') as txtfile:
               for sent in sentences:
                 txtfile.write('%s\n' % sent)
            return redirect(url_for('processed_file', filename=filename))
    return render_template('index.html')


if __name__=='__main__':
    app.run(debug=True)
