from . import home
from flask import render_template,session,template_rendered,url_for,flash,redirect,request
from app import app
from app.home.forms import LoginForm,SettingForm
import os,json
from functools import wraps
import base64
def readadmin():
    print(os.getcwd())
    f = open("config/admin.json", encoding='utf-8')
    setting = json.load(f)
    f.close()
    data = {
        "username":setting['username'],
        "password":setting['password'],
        "host":setting['host']
    }
    return data

def getuser():
    f = open("config/user.json", encoding='utf-8')
    setting = json.load(f)
    data = setting["userlist"]
    return data

def home_login_req(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if "username" in session and "password" in session:
            return f(*args , **kwargs)
        else:
            flash('请先登录！','error')
            return redirect(url_for('home.login',next = request.url))
    return decorated_function
@home.route('/')
def homepage():
    return render_template("home/home.html")
@home.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        name = data['name']
        pwd = data['pwd']
        userdata = getuser()
        for user in userdata:
            if name == user['username'] and pwd == user['password']:
                session['username'] = user['username']
                session['password'] = user['password']
                return redirect(url_for('home.index'))
        flash("账号或密码错误","error")
    return render_template("home/login.html",form = form)

@home.route('/list')
@home_login_req
def index():
    userData = getuser()
    admindata = readadmin()
    ssrdata = {}
    for user in userData:
        if user['username'] == session["username"] and user['password'] == session["password"]:
            ssrdata = user['ssr']
    ctx = {
        "ssrdata":ssrdata,
        "host":admindata['host'],
        "qrcode":"error"
    }
    return render_template("home/index.html",**ctx)

@home.route('/setting',methods = ["GET","POST"])
@home_login_req
def setting():
    form = SettingForm()
    ctx = {
        "data":session["password"]
    }
    if form.validate_on_submit():
        data = form.data
        userdata = getuser()
        for user in userdata:
            if user['username'] == session["username"]:
                user["password"] = data["password"]
        taskdata = {
            "userlist":userdata
        }
        json.dump(taskdata,open("config/user.json" ,"w"),ensure_ascii=False)
        session.pop("username")
        session.pop("password")
        return redirect(url_for('home.setting'))
    return render_template("home/setting.html",form = form,**ctx)

@home.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('username')
    session.pop("password")
    return redirect(url_for('home.login'))