from battleship import db
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime

game_user = db.Table('game_user', 
	db.Column('user_id',db.Integer,db.ForeignKey('User.id')),
	db.Column('game_id',db.Integer,db.ForeignKey('Game.id')))

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String())
    created = db.Column(db.DateTime)
    games_id = db.relationship('Game', secondary=game_user, backref = 'player', lazy='dynamic')

    def is_authenticated(self):
    	return True

    def is_active(self):
    	return True

    def is_anonymous(self):
    	return False

    def get_id(self):
    	return unicode(self.id)

    def __repr__(self):
		return '<User %r>' % self.username

    def __init__(self, username, email, password):
    	self.username = username
    	self.pwdhash = generate_password_hash(password)
    	self.email = email
    	self.created = datetime.now()

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

class Game(db.Model):
	__tablename__ = 'Game'
	id = db.Column(db.Integer, primary_key=True)
	created = db.Column(db.DateTime)
	player1 = db.relationship('User', secondary=game_user, backref = 'games_p1', lazy='dynamic')
	player2 = db.relationship('User', secondary=game_user, backref = 'games_p2', lazy='dynamic')
	moves = db.relationship('Moves', backref='game',lazy='dynamic')
	boats = db.relationship('Boats', backref='game',lazy='dynamic')
	winner = db.Column(db.Integer)

	def __repr__(self):
		return '<Game %r %r>' % (self.player1.first(), self.player2.first())

	def __init__(self,p1,p2):
		self.created = db.Column(db.DateTime)
		self.player1.append(p1)
		self.player2.append(p2)
		self.winner = -1
		self.created = datetime.now()

	def set_winner(self,player_number):
		self.winner=player_number

class Moves(db.Model):
	__tablename__ = 'Moves'
	id = db.Column(db.Integer, primary_key=True)
	x = db.Column(db.Integer)
	y = db.Column(db.Integer)
	player_number = db.Column(db.Integer)
	game_id = db.Column(db.Integer, db.ForeignKey('Game.id'))

	def __repr__(self):
		return '<Move %r %r %r %r>' % (self.x, self.y, self.player_number, self.game_id)

	def __init__(self,px,py,pnum,gameid):
		self.x = px
		self.y = py
		self.player_number = pnum
		self.game_id = gameid

class Boats(db.Model):
	__tablename__ = 'Boats'
	id = db.Column(db.Integer, primary_key=True)
	x_begin = db.Column(db.Integer)
	y_begin = db.Column(db.Integer)
	x_end = db.Column(db.Integer)
	y_end = db.Column(db.Integer)
	game_id = db.Column(db.Integer, db.ForeignKey('Game.id'))

	def __repr__(self):
		return '<Boat %r %r %r %r>' % (self.x_begin, self.x_end, self.y_begin, self.y_end, self.game_id)

	def __init__(self,x1,x2,y1,y2,gameid):
		self.x_begin = x1
		self.x_end = x2
		self.y_begin = y1
		self.y_end = y2
		self.game_id = gameid







