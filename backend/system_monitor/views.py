from system_monitor import app, db
from system_monitor.models import Post, User
from system_monitor.forms import LoginForm
from flask import request, jsonify, redirect, url_for, flash, render_template, Markup
from flask_login import current_user, login_user, logout_user
from sqlalchemy import desc
from werkzeug.security import check_password_hash
from datetime import datetime


@app.route('/')
@app.route('/index/')
def index():
    posts = [post for post in Post.query.order_by(desc(Post.created)).all()]
    safe_body = [Markup(p.body) for p in posts]
    form = LoginForm()
    return render_template('index.html', posts=posts, title='BlueBox System Monitor')


@app.route('/post/<id>')
def post_id(id):
    post = Post.query.filter_by(id=id).first_or_404()
    return render_template('posts.html', post=post)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash(f'You are now logged in as {user.username}')
        return redirect(url_for('admin.index'))
    else:
        return render_template('login.html', title='Log In', form=form)


@app.route('/logout/')
def logout():
    logout_user()
    return jsonify({"User status": "Logged out"})


