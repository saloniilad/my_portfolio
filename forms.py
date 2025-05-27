from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, URL, Optional

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=100)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send Message')

class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=2000)])
    technologies = StringField('Technologies Used', validators=[DataRequired(), 
                                                            Length(min=3, max=255)])
    github_link = StringField('GitHub Link', validators=[Optional(), URL()])
    demo_link = StringField('Live Demo Link', validators=[Optional(), URL()])
    category = SelectField('Category', choices=[
        ('web', 'Web Application'),
        ('mobile', 'Mobile App'),
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('other', 'Other')
    ])
    featured = BooleanField('Feature on Home Page')
    submit = SubmitField('Save Project')
