from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, HiddenField, TextAreaField, SelectField
from wtforms.validators import Required, Length

class MindForm(Form):
    mind = TextAreaField(validators = [Required()])
    submit = SubmitField('Send')

class MindCommentForm(Form):
    comment = StringField(validators = [Required()])
    mind_id = StringField()
    submit = SubmitField('Reply')

class ArticleForm(Form):
    title = StringField(validators = [Required(), Length(1, 128)])
    category = SelectField('Category', coerce=int)
    content = TextAreaField(validators = [Required()])
    submit = SubmitField('Publish')

class ArticleCommentForm(Form):
    comment = TextAreaField(validators = [Required()])
    article_id = StringField()
    submit = SubmitField('Reply')