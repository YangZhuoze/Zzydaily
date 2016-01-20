# -*- coding: utf-8 -*-
import hashlib, bleach
from datetime import datetime
from markdown import markdown
from flask.ext.login import UserMixin
from . import db, login_manager

class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    uuid = db.Column(db.String(64), unique = True, index = True)
    name = db.Column(db.String(64), unique = True, index = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    location = db.Column(db.String(32))
    description = db.Column(db.String(128))
    avatar = db.Column(db.String(128))
    url = db.Column(db.String(128))
    gender = db.Column(db.String(2))
    regdate = db.Column(db.DateTime, default = datetime.now())
    lasttime = db.Column(db.DateTime, default = datetime.now())
    articles = db.relationship('Article', backref = 'author', lazy = 'dynamic')
    minds = db.relationship('Mind', backref = 'author', lazy = 'dynamic')
    article_comments = db.relationship('Article_Comment', backref = 'author', lazy = 'dynamic')
    mind_comments = db.relationship('Mind_Comment', backref = 'author', lazy = 'dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.role = Role.query.filter_by(default = True).first()

    def __repr__(self):
        return '<User %r>' % self.name

    def ping(self):
        self.lasttime = datetime.now()
        db.session.add(self)

class Role(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), unique = True)
    permission = db.Column(db.Integer)
    default = db.Column(db.Boolean(), default = False)
    users = db.relationship('User', backref = 'role', lazy = 'dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True, nullable = False)
    articles = db.relationship('Article', backref = 'category', lazy = 'dynamic')

    def __repr__(self):
        return '<Category %r>' % self.name

class Article(db.Model):

    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(128), nullable = False)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, default = datetime.now())
    views_count = db.Column(db.Integer, default = 0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    comments = db.relationship('Article_Comment', backref = 'article', lazy = 'dynamic')

    def __repr__(self):
        return '<Article %r>' % self.title

class Mind(db.Model):

    __tablename__ = 'minds'

    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text)
    content_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Mind_Comment', backref = 'mind', lazy = 'dynamic')

    def __repr__(self):
        return '<Mind %r>' % self.content

    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        target.content_html = bleach.clean(value, tags = ['code', 'a'], strip = True)

class Article_Comment(db.Model):

    __tablename__ = 'article_comments'

    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime, default = datetime.now())
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))

class Mind_Comment(db.Model):

    __tablename__ = 'mind_comments'

    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime, default = datetime.now())
    content = db.Column(db.Text)
    content_html = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mind_id = db.Column(db.Integer, db.ForeignKey('minds.id'))

    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        target.content_html = bleach.clean(value, tags = ['code', 'a'], strip = True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Permission():
    PERMISSION_MIND_INSERT = 0x000001
    PERMISSION_MIND_MODIFY = 0x000002
    PERMISSION_MIND_COMMENT_INSERT = 0x000004
    PERMISSION_MIND_COMMENT_MODIFY = 0x000008
    PERMISSION_ARTICLE_INSERT = 0x000010
    PERMISSION_ARTICLE_MODIFY = 0x000020
    PERMISSION_ARTICLE_COMMENT_INSERT = 0x000040
    PERMISSION_ARTICLE_COMMENT_MODIFY = 0x000080
    PERMISSION_ARTICLE_CATEGORY_INSERT = 0x000100
    PERMISSION_ARTICLE_CATEGORY_MODIFY = 0x000200
    PERMISSION_MESSAGE_INSERT = 0x000400
    PERMISSION_MESSAGE_MODIFY = 0x000800
    PERMISSION_ALBUM_INSERT = 0x001000
    PERMISSION_ALBUM_MODIFY = 0x002000
    PERMISSION_ALBUM_COMMENT_INSERT = 0x004000
    PERMISSION_ALBUM_COMMENT_MODIFY = 0x008000
    PERMISSION_CAMERA_ACCESS = 0x010000

db.event.listen(Mind.content, 'set', Mind.on_changed_content)
db.event.listen(Mind_Comment.content, 'set', Mind_Comment.on_changed_content)

def generate():
    role = Role(name = 'Admin',permission = 0xFFFFFF, default = True)
    role2 = Role(name = 'none', permission = 0, default = False)
    db.session.add(role)
    db.session.add(role2)
    db.session.commit()
    role = Role.query.filter_by(id = 1).first()
    role2 = Role.query.filter_by(id = 1).first()
    user = User(uuid = '1',name = 'yangz',
        location = 'guangzhou', description = 'im yangzz')
    user2 = User(uuid = '2',name = 'yy',
        location = 'guangzhou', description = 'im yy')
    user2.role = role2
    db.session.add(user)
    db.session.add(user2)
    db.session.commit()
    cc = ['test', '中文', '中文+english']
    for c in cc:
        a = Category(name = c)
        db.session.add(a)
    db.session.commit()