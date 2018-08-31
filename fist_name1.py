import os
import time
from datetime import timedelta

from flask import Flask
from flask import (
    render_template, request, session
)
from werkzeug.utils import secure_filename

from bdpf.service import checkservice, Grouping

# bp = Blueprint('auth', __name__, url_prefix='/auth')
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


# 吴迪提供
# def login_required(view):
#     """View decorator that redirects anonymous users to the login page."""
#
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))
#
#         return view(**kwargs)
#
#     return wrapped_view
#
#
# @bp.before_app_request
# def load_logged_in_user():
#     """If a user id is stored in the session, load the user object from
#     the database into ``g.user``."""
#     user_id = session.get('user_id')
#
#     if user_id is None:
#         g.user = None
#     else:
#         g.user = get_db().execute(
#             'SELECT * FROM user WHERE id = ?', (user_id,)
#         ).fetchone()
#
#
# @bp.route('/register', methods=('GET', 'POST'))
# def register():
#     """Register a new user.
#
#     Validates that the username is not already taken. Hashes the
#     password for security.
#     """
#     session.clear()
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         db = get_db()
#         error = None
#
#         if not username:
#             error = '请输入用户名！'
#         elif not password:
#             error = '请输入密码！'
#         elif db.execute(
#                 'SELECT id FROM user WHERE username = ?', (username,)
#         ).fetchone() is not None:
#             error = '用户 {0} 已存在！'.format(username)
#
#         if error is None:
#             # the name is available, store it in the database and go to
#             # the login page
#             db.execute(
#                 'INSERT INTO user (username, password) VALUES (?, ?)',
#                 (username, generate_password_hash(password))
#             )
#             db.commit()
#             return redirect(url_for('auth.login'))
#
#         flash(error)
#
#     return render_template('auth/register.html')
#
#
# @bp.route('/login', methods=('GET', 'POST'))
# def login():
#     """Log in a registered user by adding the user id to the session."""
#     session.clear()
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         db = get_db()
#         error = None
#         user = db.execute(
#             'SELECT * FROM user WHERE username = ?', (username,)
#         ).fetchone()
#         if not username:
#             error = '请输入用户名！'
#         elif not password:
#             error = '请输入密码！'
#         elif user is None:
#             error = '用户名错误！'
#         elif not check_password_hash(user['password'], password):
#             error = '密码错误！'
#
#         if error is None:
#             # store the user id in a new session and return to the index
#             session.clear()
#             session['user_id'] = user['id']
#             return redirect(url_for('auth.index'))
#
#         flash(error)
#
#     return render_template('auth/login.html')
#
#
# @bp.route('/logout')
# def logout():
#     """Clear the current session, including the stored user id."""
#     session.clear()
#     return redirect(url_for('auth.login'))
#
#
# @bp.route('/index')
# def index():
#     """Show all the posts, most recent first."""
#     db = get_db()
#     posts = db.execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' ORDER BY created DESC'
#     ).fetchall()
#     return render_template('auth/index.html', posts=posts)
# end wudi


if __name__ == '__main__':
    # checkservice.upload_check('123')
    # app.run(host='0.0.0.0',port=8080)
    app.run(port=8080)
