import json
import urllib2
from datetime import datetime
from flask import render_template, current_app, redirect, url_for, request
from flask.ext.login import current_user, login_required
from weibo import APIClient

from . import main
from .form import MindForm, MindCommentForm, ArticleCommentForm
from .. import db
from ..models import Mind, Article, Mind_Comment, Article_Comment, Category

@main.route('/', methods = ['GET', 'POST'])
def index():
    from ..models import User
    from flask.ext.login import login_user
    user = User.query.filter_by(id = 1).first()
    login_user(user)
    conn = urllib2.Request(current_app.config['WEATHER_API'] + current_app.config['WEATHER_CITY'])
    conn.add_header('apikey', current_app.config['APIKEY'])
    weather = json.loads(urllib2.urlopen(conn).read().decode('utf-8'))
    weather = weather.get('HeWeather data service 3.0')[0]
    minds = Mind.query.order_by(Mind.timestamp.desc()).all()
    articles = Article.query.order_by(Article.timestamp.desc()).all()
    mind_form = MindForm()
    comment_form = MindCommentForm()
    return render_template('index.html', user = current_user,
        minds = minds, articles = articles, weather = weather,
            mind_form = mind_form, comment_form = comment_form)

@main.route('/article', methods = ['GET', 'POST'])
def article():
    articles = Article.query.order_by(Article.timestamp.desc()).all()
    categories = Category.query.all()
    return render_template('article.html', articles = articles, categories = categories)

@main.route('/article/<int:id>', methods = ['GET', 'POST'])
def article_body(id):
    article = Article.query.filter_by(id = id).first()
    article.views_count = article.views_count + 1
    db.session.add(article)
    article_prev = Article.query.filter_by(id = id - 1).first()
    article_next = Article.query.filter_by(id = id + 1).first()
    comment_form = ArticleCommentForm()
    return render_template('article_body.html', article = article,
        article_prev = article_prev, article_next = article_next,
        comment_form = comment_form)

@main.route('/send/mind', methods = ['GET', 'POST'])
@login_required
def send_mind_comment():
    form = MindCommentForm()
    if form.validate_on_submit():
        comment = Mind_Comment(content = form.comment.data,
            author = current_user._get_current_object(),
            mind_id = form.mind_id.data,
            timestamp = datetime.now())
        db.session.add(comment)
        return redirect(url_for('.index'))

@main.route('/send/mind-comment', methods = ['GET', 'POST'])
@login_required
def send_mind_comment():
    form = MindCommentForm()
    if form.validate_on_submit():
        comment = Mind_Comment(content = form.comment.data,
            author = current_user._get_current_object(),
            mind_id = form.mind_id.data,
            timestamp = datetime.now())
        db.session.add(comment)
        return redirect(url_for('.index'))

@main.route('/send/article-comment', methods = ['GET', 'POST'])
@login_required
def send_article_comment():
    form = ArticleCommentForm()
    if form.validate_on_submit():
        comment = Article_Comment(body = form.comment.data,
            timestamp = datetime.now(),
            article_id = form.article_id.data)
        db.session.add(comment)
        return redirect(url_for('.article_body', id = form.article_id.data))

@main.route('/edit-article', methods = ['GET', 'POST'])
def edit_article():
    return render_template('edit_article.html')