from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,ValidationError

class LoginForm(FlaskForm):
    name = StringField(
        label="username",
        validators=[
            DataRequired("请输入用户名")
        ],
        render_kw={
            "placeholder":"请输入用户名"
        }
    )
    pwd = PasswordField(
        label='password',
        validators=[
            DataRequired('请输入密码')
        ],
        render_kw={
            'placeholder':"请输入密码"
        }
    )

class SettingForm(FlaskForm):
    password = StringField(
        label='password',
        validators=[
            DataRequired('请输入管理员密码')
        ],
        render_kw={
            "class":"tpl-form-input",
            "id":"password"
        }
    )