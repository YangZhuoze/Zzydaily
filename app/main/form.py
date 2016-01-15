from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import Required

class MindForm(Form):
    mind = TextAreaField()
    submit = SubmitField('Comment')

class MindCommentForm(Form):
    comment = StringField()
    mind_id = StringField()
    submit = SubmitField('Reply')

class ArticleCommentForm(Form):
    comment = TextAreaField()
    article_id = StringField()
    submit = SubmitField('Reply')