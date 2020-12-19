import datetime
from system_monitor import db, login
from flask import redirect, url_for
from flask_login import UserMixin, current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'{self.username}'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    author = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    body = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'{self.created}, {self.author}, {self.title}'


# Backend CLI Utility function for creating an admin
def create_admin(username, password):
    hashed_password = generate_password_hash(password)
    new_admin = User(username=username, password_hash=hashed_password)
    confirmation = input(f'Create admin {username}? Y/N ')
    if confirmation == 'Y' or 'y':
        db.session.add(new_admin)
        db.session.commit()
    else:
        db.session.rollback()
        print('Aborted')


# Backend CLI Utility function for deleting an admin
def delete_admin(username):
    admin = User.query.filter_by(username=username).first()
    confirmation = input(f'Delete admin {username}? Y/N ')
    if confirmation == 'Y' or 'y':
        db.session.delete(admin)
        db.session.commit()
    else:
        print('Aborted')


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class AdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

    
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))