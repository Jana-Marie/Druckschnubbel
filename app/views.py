import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

debug = True

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = ['txt', 'png', 'jpg', 'jpeg', 'gif']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html',
                           Dateitypen=str(app.config['ALLOWED_EXTENSIONS']).replace("[", "").replace("]", "").replace("'", "").replace(",", ", "))


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)  # check for unallowed chars
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('printing'))
    else:
        return redirect(url_for('err'))


@app.route('/templates/scratchcard.html')
def scratchcard():
    return render_template('scratchcard.html')


@app.route('/templates/', methods=['POST'])
def scratchcard_receive():
    text = request.form['text']
    return text


@app.route('/templates/printing.html')
def printing():
    return render_template('printing.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('err404.html'), 404


@app.route('/templates/error.html')
def err():
    return render_template('error.html'), 404


if __name__ == '__main__':
    if debug == False:
        app.run(
            host="0.0.0.0",
            port=int("80"),
            debug=False
        )
    else:
        app.run(
            debug=True
        )