from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, HiddenField, TextAreaField, SelectField
from wtforms.validators import Required

class MindForm(Form):
    mind = TextAreaField()
    submit = SubmitField('Send')

class MindCommentForm(Form):
    comment = StringField()
    mind_id = StringField()
    submit = SubmitField('Reply')

class ArticleForm(Form):
    title = StringField()
    category = SelectField('Category', coerce=int)
    content = TextAreaField()
    submit = SubmitField('Publish')

class ArticleCommentForm(Form):
    comment = TextAreaField()
    article_id = StringField()
    submit = SubmitField('Reply')