from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired

class signup(FlaskForm):
    name =StringField('Your Name',  validators=[Length(min=4,max=50),DataRequired()])
    email =StringField('Your Email',validators=[Email(), DataRequired()])
    password1=PasswordField("Password", validators=[Length(min=6), DataRequired()])
    password2=PasswordField("Repeat Password", validators=[EqualTo("password1"), DataRequired()])
    submit=SubmitField("Submit")



    