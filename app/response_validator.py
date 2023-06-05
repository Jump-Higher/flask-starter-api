from flask_inputs import Inputs
from wtforms.validators import DataRequired, Email, Length, Regexp

class validator_user(Inputs):
    json = {
        "name": [DataRequired(message='Name is Required'), Length(max=50, message='Name Must not Exceed 50 Character')],
        "username": [DataRequired(message='Username is Required'), Length(min=5, max=12, message='Username Must be Between 5 and 12 Characters')],
        "email": [DataRequired(message='Email is Required'), Email(message='Invalid Email Format')],
        "password": [DataRequired(message='Password is Required'), Length(min=8, max=20, message='Password Must be Between 8 and 20 Characters')]
    }

class validator_update_user(Inputs):
    form = {
        "name": [DataRequired(message='Name is Required'), Length(max=50, message='Name Must not Exceed 50 Character')],
        "username": [DataRequired(message='Username is Required'), Length(min=5, max=12, message='Username Must be Between 5 and 12 Characters')],
        "email": [DataRequired(message='Email is Required'), Email(message='Invalid Email Format')],
        "password": [DataRequired(message='Password is Required'), Length(min=8, max=20, message='Password Must be Between 8 and 20 Characters')],
        "address": [DataRequired(message='Address is Required')]
    }


