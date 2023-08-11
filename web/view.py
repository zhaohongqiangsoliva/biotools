from app import app, db

# 网站首页
from app.forms import RegisterForm, LoginForm
from flask import render_template, flash, redirect, url_for, session

from app.models import User


@app.route('/')
def index():
    return 'index'


# 注册页面
@app.route('/register/', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 1. 从前端获取用户输入的值;
        email = form.email.data
        username = form.username.data
        password = form.password.data

        # 2. 判断用户是否已经存在? 如果返回位None，说明可以注册;
        u = User.query.filter_by(username=username).first()
        if u:
            flash("用户%s已经存在" % (u.username))
            return redirect(url_for('register'))
        else:
            u = User(username=username, email=email)
            u.password = password
            db.session.add(u)
            db.session.commit()
            flash("注册用户%s成功" % (u.username))
            return redirect(url_for('login'))
    return render_template('register.html',
                           form=form)


# 登录页面
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # 1. 判断用户是否存在?
        u = User.query.filter_by(username=username).first()
        if u and u.verify_password( password):
            session['user_id'] = u.id
            session['user'] = u.username
            flash("登录成功!")
            return  redirect(url_for('index'))
        else:
            flash("用户名或者密码错误!")
            return  redirect(url_for('login'))

    return  render_template('login.html',
                            form=form)

@app.route('/logout/')
def logout():
    session.pop('user_id', None)
    session.pop('user', None)

    return  redirect(url_for('login'))


# 添加任务
@app.route('/todo/add/')
def todo_add():
    return 'todo_add'


# 编辑任务
@app.route('/todo/edit/<int:id>/')
def todo_modify(id):
    return "todo_modify %s" % (id)


# 删除任务
@app.route('/todo/delete/<int:id>/')
def todo_delete(id):
    return "todo_delete"


# 查看任务
@app.route('/todo/list/')
@app.route('/todo/list/<int:page>')
def list(page):
    return "list"


# 修改任务状态为完成
@app.route('/todo/done/<int:id>/')
def done(id):
    return 'done'


# 修改任务状态为未完成
@app.route('/todo/undo/<int:id>')
def undo(id):
    return 'undo'
