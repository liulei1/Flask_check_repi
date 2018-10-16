import functools
import json
import os
import time
from datetime import timedelta
from typing import List

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, make_response, send_from_directory, Response
from flask import (
    flash, g, redirect, render_template, request, session, url_for
)
from flask.json import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

import db
from bdpf.dao import ETLProcess
from bdpf.model.ProcessedInfo import ProcessedInfo
from bdpf.service import CheckService, CheckAlgorithm, ReceivedService, MetaDataService
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


# 拦截请求-用户未登录跳转至登陆界面
# @app.before_request
# def load_logged_in_user():
#     if not request.path == '/login' and not request.path == '/to_login' and not request.path.startswith("/static"):
#         user_id = session.get('user_id')
#         if user_id is None:
#             return redirect(url_for("login_page"))
#         else:
#             g.user = get_db().execute(
#                 'SELECT * FROM user WHERE id = ?', (user_id,)
#             ).fetchone()


# 用户登陆
@app.route('/login', methods=('GET', 'POST'))
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
            session['user_name'] = user['username']
            return redirect(url_for("home_page"))
        flash(error)
    return render_template('login.html')


# 用户注册
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


@app.route('/home_page', methods=['GET', 'POST'], strict_slashes=False)
def home_page():
    return render_template('home.html')


@app.route('/to_login', methods=['GET', 'POST'], strict_slashes=False)
def login_page():
    session.clear()
    return render_template('login.html')


@app.route('/to_upload', methods=['GET'], strict_slashes=False)
def index_page():
    return render_template('file_upload.html')


@app.route('/to_update', methods=['GET'], strict_slashes=False)
def update_page():
    return render_template('update_upload.html')


# 用户申请-文件上传
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
        res_list = CheckService.upload_check(f_path)
        # 将查重结果的list进行分类，入参一个list，返回含有三个list的数组。
        # 将分类后的查重结果进行展示。
        arr: tuple = CheckAlgorithm.table_group(res_list)
        # return render_template('result.html', match=arr[0], unmatch=arr[1], maybe=arr[2])
        match_list = arr[1]
        match_list.extend(arr[2])
        return render_template('result.html', match=match_list, unmatch=arr[0])
        # return "上传成功"
    else:
        return "上传文件失败"


# 已受理查看
@app.route('/show_received', methods=['GET', 'POST'], strict_slashes=False)
def show_received():
    received_list = ReceivedService.query_received_table()
    return render_template('received.html', received_list=received_list)


# 查重提交-不重复表
@app.route('/user_submit', methods=['GET', 'POST'], strict_slashes=False)
def user_submit():
    json_str = request.form.get("submit_json")
    json_data = json.loads(json_str)
    print(json_data)
    json_list = json_data["arr"]
    user_name = session.get("user_name")
    res = ReceivedService.receive_submit(json_list, user_name)
    return res


# 条件查询已受理
@app.route('/received_query', methods=['POST'], strict_slashes=False)
def received_query():
    t_name = request.form['t_name']
    t_cname = request.form['t_cname']
    received_list = ReceivedService.query_received_table(t_name, t_cname)
    return render_template('received.html', received_list=received_list)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return view(**kwargs)

    return wrapped_view


# 允许上传的文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_session():
    new_filename = session.get('new_filename')
    print(new_filename)
    return new_filename or u'no session'


# 更新已受理信息
@app.route('/update_received', methods=['POST'], strict_slashes=False)
def update_received():
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
        updated_list: List[ProcessedInfo] = CheckService.upload_update(f_path)
        return render_template('update_result.html', updated_list=updated_list)
    else:
        return "上传文件失败"


# 文件下载
@app.route('/download/<path:filename>')
def download_file(filename):
    # directory = os.getcwd()
    directory = os.path.join(app.root_path, 'static')
    # as_attachment表示下载
    response: Response = make_response(send_from_directory(directory, filename, as_attachment=True))
    print(type(response))
    response.headers["Content-Disposition"] = "attachment;filename={}".format(filename)
    return response


# 生成元数据
@app.route('/generate_metadata', methods=['GET', 'POST'])
def generate_metadata():
    print("generate_metadata..........")
    # need_generate_count, generate_count, generate_list = ETLProcess.generate_etl_data()
    need_generate_count, generate_count, generate_list = MetaDataService.generate_meta();
    return render_template('meta_generate_result.html', need_generate_count=need_generate_count,
                           generate_count=generate_count,
                           generate_list=generate_list)


# 生成元数据-json
@app.route('/generate_metadata_json', methods=['GET', 'POST'])
def generate_metadata_json():
    print("generate_metadata..........")
    need_generate_count, generate_count, generate_list = ETLProcess.generate_etl_data()
    # res = ["200", need_generate_count, generate_count]
    # return json.dumps(res)
    return jsonify({'state': 200, 'need_generate_count': need_generate_count, 'generate_count': generate_count})


def generate_meta_schedule():
    print("generate meta ok ...")


if __name__ == '__main__':
    # checkservice.upload_check('123')
    # app.run(host='0.0.0.0',port=8080)
    # schedule.every(1).minutes.do(test_schedule)

    # 定时执行元数据生成
    scheduler = BackgroundScheduler()
    # scheduler.add_job(test_schedule, 'cron', hour='0', minute='1', second='0')
    scheduler.add_job(func=generate_meta_schedule, trigger='interval', minutes=1)
    # 启动调度器，到点task就会被执行啦
    scheduler.start()
    app.run(port=8080)
