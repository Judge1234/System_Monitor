from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin 
from flask_login import LoginManager
from .momentjs import momentjs


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1q2w3e4rR@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'readable'
db = SQLAlchemy(app)
app.jinja_env.globals['momentjs'] = momentjs

login = LoginManager(app)

from system_monitor import views
from system_monitor.models import *

admin_suite = Admin(app,  name='BlueBox Monitoring System', 
                    template_mode='bootstrap3',
                    index_view=AdminView())

admin_suite.add_view(AdminModelView(Post, db.session))
admin_suite.add_view(AdminModelView(User, db.session))

