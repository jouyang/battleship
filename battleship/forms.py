from wtforms import Form, BooleanField, TextField, PasswordField, validators, IntegerField

class LoginForm(Form):
	username = TextField('Username', [validators.Length(min=4, max=25)])
	password = PasswordField('Password',[validators.Required()])

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35),validators.Email(message='Invalid Email Address')])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=6, max=20)
    ])
    confirm = PasswordField('Repeat Password')

class ChallengeForm(Form):
	username = TextField('Opponent', [validators.Length(min=4, max=25)])
	ship1x = IntegerField('Ship 1 X:', [validators.NumberRange(min=0, max=6, message='The sea is only 6X6!')])
	ship1y = IntegerField('Ship 1 Y:', [validators.NumberRange(min=0, max=6, message='The sea is only 6x6!')])
	ship2x = IntegerField('Ship 2 X:', [validators.NumberRange(min=0, max=6, message='The sea is only 6x6!')])
	ship2y = IntegerField('Ship 2 Y:', [validators.NumberRange(min=0, max=6, message='The sea is only 6x6!')])
	ship3x = IntegerField('Ship 3 X:', [validators.NumberRange(min=0, max=6, message='The sea is only 6x6!')])
	ship3y = IntegerField('Ship 3 Y:', [validators.NumberRange(min=0, max=6, message='The sea is only 6x6!')])

class CreateGameForm(Form):
	ship1x = IntegerField('Ship 1 X:', [validators.NumberRange(min=0, max=6, message='The sea is only 6x6!')])
	ship1y = IntegerField('Ship 1 Y:', [validators.NumberRange(min=0, max=6, message='The sea is only 6x6!')])
	ship2x = IntegerField('Ship 2 X:', [validators.NumberRange(min=0, max=6, message='The sea is only 6x6!')])
	ship2y = IntegerField('Ship 2 Y:', [validators.NumberRange(min=0, max=6, message='The sea is only 6x6!')])
	ship3x = IntegerField('Ship 3 X:', [validators.NumberRange(min=0, max=6, message='The sea is only 6x6!')])
	ship3y = IntegerField('Ship 3 Y:', [validators.NumberRange(min=0, max=6, message='The sea is only 6x6!')])