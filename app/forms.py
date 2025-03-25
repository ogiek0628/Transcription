from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    file = FileField('Choose a file', validators=[DataRequired()])
    submit = SubmitField('Upload')
