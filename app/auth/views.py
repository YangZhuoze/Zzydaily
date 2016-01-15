import urllib2
from flask import session, redirect, request, url_for, flash, current_app
from flask.ext.login import login_user, logout_user, login_required, current_user
from weibo import APIClient

from . import auth
from .forms import LoginForm, RegisterForm
from .. import db
from ..models import User

@auth.route('/login', methods = ['GET'])
def login():
    client = APIClient(
        app_key = current_app.config['APP_KEY'],
        app_secret = current_app.config['APP_SECRET'],
        redirect_uri = current_app.config['CALLBACK_URL'])
    url = client.get_authorize_url()
    return redirect(url)

@auth.route('/callback', methods = ['GET', 'POST'])
def callback():
    code = request.args.get('code')
    if code is not None:
        client = APIClient(
            app_key = current_app.config['APP_KEY'],
            app_secret = current_app.config['APP_SECRET'],
            redirect_uri = current_app.config['CALLBACK_URL'])
        r = client.request_access_token(code)
        access_token = r.access_token
        expires_in = r.expires_in
        uid = r.uid
        client.set_access_token(access_token, expires_in)
        session['access_token'] = access_token
        user = User.query.filter_by(uuid = uid).first()
        if user is not None:
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            u = client.users.show.get(uid = uid)
            user = User(
                uuid = uid,
                name = u.get('screen_name'),
                location = u.get('location'),
                description = u.get('description'),
                avatar = u.get('profile_image_url'),
                url = u.get('domain'),
                gender = u.get('gender')
            )
            db.session.add(user)
            login_user(user)
            return redirect(url_for('main.index'))
    else:
        return redirect(url_for('main.index'))

@auth.route('/logout')
@login_required
def logout():
    '''
        I still do not know why I can not access the g.client
        when I set g.client = client in the callback().
        I think that they are in the same request..well not quite sure about that
    '''
    current_user.ping()
    logout_user()
    access_token = session['access_token']
    http_url = 'https://api.weibo.com/oauth2/revokeoauth2?access_token=%s' % access_token
    req = urllib2.Request(http_url)
    req.add_header('Accept-Encoding', 'gzip')
    req.add_header('Authorization', 'OAuth2 %s' % access_token)
    urllib2.urlopen(req)
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

'''
    The original version of the website had a independent account module,
    after a few weeks coding, I think that is not easy enough for a new user,
    so I change the independent login pattern into login through sina weibo.
    the register module will no long existed.

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data)
        db.session.add(user)
        user = User.query.filter_by(username = form.username.data).first()
        login_user(user)
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('auth/register.html', form = form)
'''