# forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

# Login form for manual username/password login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# Form for creating a new article post
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    author = StringField('Author', validators=[DataRequired(), Length(max=100)])
    body = TextAreaField('Body', validators=[DataRequired()])
    image_path = FileField(
        'Image',
        validators=[
            FileRequired(message="Please upload an image."),
            FileAllowed(['jpg', 'png'], 'Only .jpg or .png images are allowed!')
        ]
    )
    submit = SubmitField('Save Article')
