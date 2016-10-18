from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm,RegistrationForm,ChangePassword
from models import User, Role
#from email import *
import email
#raise Exception("######\n %s \n########" % dir(email))

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    # if g.user.is_authenticated and not g.user.confirmed :
    # #             # and request.endpoint[:5] != 'auth.' \
    # #             # and request.endpoint != 'static':
    return redirect(url_for('unconfirmed'))


@app.route('/unconfirmed')
def unconfirmed():
    if g.user.is_anonymous or g.user.confirmed:
        return redirect(url_for('index'))
    return render_template('unconfirmed.html')

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
        title = 'Home',
        user = user,
        posts = posts)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash('Invalid login. Please try again.')
    return render_template('login.html',
        title = 'Sign In',
        form = form,
        )



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data,confirmed = False)
        db.session.add(user)
        db.session.commit()
        token =user.generate_confirmation_token()
        email.send_email(user.email, 'Confirm Your Account','email/confirm',user = user, token = token)
        flash('A Confirmation email has been sent to you by email')

   #     flash('You can now login.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thank You!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first()
    if user == None:
        flash('User %s not found' %username)
        return redirect(url_for('index'))
    posts = [
        {'author':user, 'body':'Test post #1'},
        {'author':user, 'body':'Test post #2'}
    ]
    return render_template('user.html', user = user, posts = posts)

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def Change_Password():
    form = ChangePassword()
    if form.validate_on_submit():
        if g.user.verify_password(form.old_password.data):
            g.user.password = form.new_password.data
            db.session.add(g.user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('index'))
        else:
            flash('Invalid password.')
    return render_template('change-password.html', form=form)
