import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Email, Length, EqualTo, ValidationError, DataRequired

def character_check(form,field):
    excluded_chars = "*?!'^+%&/()=}][{$#@<>"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed.")


class RegisterForm(FlaskForm):
    firstname = StringField(validators=[character_check])
    lastname = StringField(validators=[character_check])
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(), Length(min=6, max=12, message='Password must be betweem 6 and 12 characters in length.')])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password', message='Both password fields must be equal.')])
    submit = SubmitField()


    def validate_password(self, password):
        pw = re.compile(r'(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}')
        if not pw.match(self.password.data):
            raise ValidationError("Password must contain at least 1 Digit, 1 Lowercast Character, 1 Uppercase Character & 1 Special Character.")


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()