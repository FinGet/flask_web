from flask import Flask, render_template, request
import os
import pathlib
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 

# SRC_PATH = os.path.dirname(os.path.abspath(__file__)) # python 3.3-
SRC_PATH = pathlib.Path(__file__).parent.absolute() # python 3.4+
UPLOAD_FOLDER = os.path.join(SRC_PATH, 'uploads')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_filename(filename):
  return filename.rsplit('.', 1)[0]

@app.route('/')
def hello_world():
  return render_template('index.html')

@app.route('/test')
def test():
  items = ['apple', 'banana', 'coconut']
  return render_template('test.html', username='FinGet', date='2024-01-01', items=items)

@app.route('/upload', methods=['POST'])
def upload_file():
  file = request.files['filename']
  if file and allowed_file(file.filename):
    file.save(os.path.join(file.filename))
    return render_template('test.html', filename=file.filename)
  else:
    error_msg = 'Sorry, file type not allowed.'
    return render_template('404.html', error_msg=error_msg), 400

@app.errorhandler(413)
def request_entity_too_large(error):
  error_msg = 'Sorry, file size too large.'
  return render_template('404.html', error_msg=error_msg), 413

@app.errorhandler(404)
def page_not_found(error):
  error_msg = 'Sorry, page not found.'
  return render_template('404.html', error_msg=error_msg), 404

if __name__ == '__main__':
  app.run(debug=True)

