from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import LoginForm
from .. import db
from ..models import User

@main.route('/', methods = ['GET','POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('.index')) #'.index' = 'main.index'
        else:
            flash('Invalid login. Please try again.')
    return render_template('index.html', form = form,
                            name = session.get('name'),
                            known=session.get('known', False),
                            current_time=datetime.utcnow())

