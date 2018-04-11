from flask import Flask
import os

app = Flask(__name__)
app.debug = False
app.config['SECRET_KEY'] = '183449eb77e74f5e8c2023d09a1c1734'
from app.admin import admin as admin_blueprint
from app.home import home as home_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix = '/admin')