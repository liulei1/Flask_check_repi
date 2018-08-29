import os
import time
from datetime import timedelta

from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename

from bdpf.service import checkservice

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['xlsx'])


@app.route('/',methods=['GET'], strict_slashes=False)
def index_page():
    return render_template('index.html')


@app.route('/', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['file']

    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        ext = fname.rsplit('.',1)[1]
        unix_time = int(time.time())
        new_filename = str(unix_time)+'.'+ ext
        f.save(os.path.join(file_dir,new_filename))
        f_path = file_dir+'/'+new_filename
        print(f_path)
        res_list = checkservice.upload_check(f_path)
        return render_template('result.html', res=res_list)
        # return "上传成功"
    else:
        return "上传文件失败"


@app.route('/loginin', methods=['POST'])
def sign_in():
    username = request.form['username']
    password = request.form['password']
    if username == 'xuyunlong' and password == '123456':
        return render_template('signin-ok.html', username=username)
    return render_template('form.html', message='Bad username or password', username=username)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_session():
    new_filename = session.get('new_filename')
    print(new_filename)
    return new_filename or u'no session'


if __name__ == '__main__':
    # checkservice.upload_check('123')
    # app.run(host='0.0.0.0',port=8080)
    app.run(port=8080)