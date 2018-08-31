import os
import time
from datetime import timedelta
import functools
from flask import Flask
from flask import (
    flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from bdpf.service import checkservice, Grouping
import db
from db import get_db

app = Flask(__name__)

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
app.config.from_mapping(
    # store the database in the instance folder
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['xlsx'])
db.init_app(app)


@app.route('/', methods=('GET', 'POST'))
def login():
    session.clear()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        if not username:
            error = '请输入用户名！'
        elif not password:
            error = '请输入密码！'
        elif user is None:
            error = '用户名错误！'
        elif not check_password_hash(user['password'], password):
            error = '密码错误！'

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index_page'))

        flash(error)

    return render_template('login.html')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = '请输入用户名！'
        elif not password:
            error = '请输入密码！'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = '用户 {0} 已存在！'.format(username)

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('login'))

        flash(error)

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/index', methods=['GET'], strict_slashes=False)
def index_page():
    return render_template('index.html')


@app.route('/file_upload', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['file']

    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        ext = fname.rsplit('.', 1)[1]
        unix_time = int(time.time())
        new_filename = str(unix_time) + '.' + ext
        f.save(os.path.join(file_dir, new_filename))
        f_path = file_dir + '/' + new_filename
        print(f_path)
        res_list = checkservice.upload_check(f_path)
        # 将查重结果的list进行分类，入参一个list，返回含有三个list的数组。
        # 将分类后的查重结果进行展示。
        arr = Grouping.GenGroup(res_list)
        # return render_template('result.html', match=arr[0], unmatch=arr[1], maybe=arr[2])
        match_list = arr[1]
        match_list.extend(arr[2])
        return render_template('result.html', match=match_list, unmatch=arr[0])
        # return "上传成功"
    else:
        return "上传文件失败"


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
