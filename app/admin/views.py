from . import admin
from flask import render_template,session,template_rendered,url_for,flash,redirect,request
from app.admin.forms import LoginForm,SettingForm,AddportForm,AdduserForm
from app import app
import json,os
from functools import wraps
def readadmin():
    f = open("config/admin.json", encoding='utf-8')
    setting = json.load(f)
    f.close()
    data = {
        "username":setting['username'],
        "password":setting['password'],
        "host":setting['host']
    }
    return data
def ssrlist():
    f = open("/etc/shadowsocks-r/config.json",encoding='utf-8')
    # 发起请求
    ssrinfo = json.load(f)
    return ssrinfo
def getuser():
    f = open("config/user.json", encoding='utf-8')
    setting = json.load(f)
    data = setting["userlist"]
    return data
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if "islogin" in session:
            return f(*args , **kwargs)
        else:
            flash('请先登录','error')
            return redirect(url_for('admin.login',next = request.url))
    return decorated_function

@admin.route('/list')
@admin_login_req
def index():
    form = AdduserForm()
    jsonData = getuser()
    ctx = {
        "userinfo":jsonData,
    }
    return render_template("admin/list.html",**ctx,form = form)

@admin.route('/',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        name = data['name']
        pwd = data['pwd']
        admin = readadmin()
        if name == admin['username'] and pwd == admin['password']:
            session['islogin'] = admin['username']
            return redirect(url_for('admin.index'))
        else:
            flash("账号或密码错误","error")
    return render_template("admin/login.html",form = form)

@admin.route('/portlist')
@admin_login_req
def portlist():
    form = AddportForm()
    info = ssrlist()
    ctx = {
        "portlist":info,
    }
    return render_template("admin/portlist.html",**ctx,form = form )

@admin.route('/setting',methods = ["GET","POST"])
@admin_login_req
def setting():
    form = SettingForm()
    ctx = {
        "data":readadmin()
    }
    if form.validate_on_submit():
        data = form.data
        json.dump(data,open("config/admin.json" ,"w"),ensure_ascii=False)
        return redirect(url_for('admin.setting'))
    return render_template("admin/setting.html",form = form,**ctx)

@admin.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('islogin')
    return redirect(url_for('admin.login'))

@admin.route('/deluser/<username>')
@admin_login_req
def deluser(username):
    userdata = getuser()
    for user in range(0,len(userdata)):
        if userdata[user]["username"] == username:
            userdata.pop(user)
            data = {
                "userlist":userdata
            }
            json.dump(data,open("config/user.json" ,"w"),ensure_ascii=False)
            return redirect(url_for('admin.index'))
    return redirect(url_for('admin.index'))

@admin.route('/adduser',methods = ["POST"])
@admin_login_req
def adduser():
    form = AddportForm()
    if form.validate_on_submit:
        if form.data['name'].strip(" ") == "" or form.data['pwd'].strip(" ") == "":
            flash("用户名密码不合法","error")
            return redirect(url_for("admin.userlist"))
        userdata = getuser()
        for user in userdata:
            if user['username'] == form.data['name']:
                flash("已经存在相同的用户","error")
                return redirect(url_for("admin.userlist"))
        newuserdata = {
            "username":form.data['name'],
            "password":form.data['pwd'],
            "ssr":{
                "port":"",
                "password":"",
                "method": "",
                "protocol": "",
                "obfs": ""
            }
        }
        userdata.append(newuserdata)
        data = {
            "userlist":userdata
        }
        json.dump(data,open("config/user.json" ,"w"),ensure_ascii=False)
        return redirect(url_for('admin.index'))

@admin.route('/addport',methods = ["POST"])
@admin_login_req
def addport():
    form = AddportForm()
    if form.validate_on_submit:
        if form.data['name'].strip(" ") == "" or form.data['pwd'].strip(" ") == "":
            flash("端口或密码不合法","error")
            return redirect(url_for("admin.portlist"))
        ssr = ssrlist()
        ssr['port_password'][form.data['name']] = form.data['pwd']
        json.dump(ssr,open("/etc/shadowsocks-r/config.json" ,"w"),ensure_ascii=False)
        os.system("/etc/init.d/shadowsocks-r restart")
        return redirect(url_for('admin.portlist'))

@admin.route('/delport/<port>')
@admin_login_req
def delport(port):
    ssrdata = ssrlist()
    try:
        ssrdata['port_password'].pop(port)
    except:
        flash("端口错误","error")
    json.dump(ssrdata,open("/etc/shadowsocks-r/config.json" ,"w"),ensure_ascii=False)
    os.system("/etc/init.d/shadowsocks-r restart")
    return redirect(url_for('admin.portlist'))

@admin.route("/addssr/<username>/<port>")
@admin_login_req
def addssr(username,port):
    configdata = ssrlist()
    data = {
        "port":port,
        "password":configdata['port_password'][port],
        "method": configdata['method'],
        "protocol": configdata['protocol'],
        "obfs": configdata['obfs']
    }
    userdata = getuser()
    for i in userdata:
        if i['username'] == username:
            i['ssr'] = data
    alldata = {
        "userlist":userdata
    }
    json.dump(alldata,open("config/user.json" ,"w"),ensure_ascii=False)
    return redirect(url_for("admin.portlist"))