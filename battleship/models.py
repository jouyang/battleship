from battleship import db
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import UniqueConstraint

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String())
    created = db.Column(db.DateTime)
    moves = db.relationship('Moves', backref='player_move',lazy='dynamic')
    ships = db.relationship('Ships', backref='player_ship',lazy='dynamic')

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
	id = db.Column(db.Integer, primary_key=True)
	player1 = db.Column(db.Integer)
	player2 = db.Column(db.Integer)
	moves = db.relationship('Moves', backref='source',lazy='dynamic')
	ships = db.relationship('Ships', backref='source',lazy='dynamic')
	winner = db.Column(db.Integer)
	ready = db.Column(db.Boolean)
	turn = db.column(db.Integer)

	__table_args__ = (UniqueConstraint('player1','player2',name='u12'),)

	def __repr__(self):
		return '<Game %r %r>' % (self.player1, self.player2)

	def __init__(self,p1,p2):
		self.created = db.Column(db.DateTime)
		self.player1 = p1
		self.player2 = p2
		self.winner = -1
		self.created = datetime.now()
		self.ready = False
		self.turn = -1

	def set_ready(self):
		if len(self.ships.all())==6:
			self.ready = True

	def set_winner(self,player_number):
		self.winner=player_number

	def change_turn(self):
		if self.turn == -1:
			self.turn = self.player1
		elif self.turn == self.player1:
			self.turn = self.player2
		else:
			self.turn = self.player1

class Moves(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	x = db.Column(db.Integer)
	y = db.Column(db.Integer)
	player_id = db.Column(db.Integer,db.ForeignKey('user.id'))
	game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
	hit= db.Column(db.Boolean)
	__table_args__ = (UniqueConstraint('x','y','game_id','player_id',name='u_xy_m'),)

	def __repr__(self):
		return '<Move %r %r %r %r>' % (self.x, self.y, self.player_id, self.game_id)

	def __init__(self,px,py,pnum,gameid):
		self.x = px
		self.y = py
		self.player_id = pnum
		self.game_id = gameid
		self.created = datetime.now()
		self.hit = False

	def checkhit(self):
		self.hit = True


class Ships(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	x= db.Column(db.Integer)
	y= db.Column(db.Integer)
	player_id = db.Column(db.Integer,db.ForeignKey('user.id'))
	game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
	hit = db.Column(db.Boolean)
	__table_args__ = (UniqueConstraint('x','y','game_id','player_id',name='u_xy_b'),)

	def __repr__(self):
		return '<Boat %r %r %r %r>' % (self.x, self.y, self.player_id, self.game_id)

	def __init__(self,x,y,player,gameid):
		self.x = x
		self.y = y
		self.player_id = player
		self.game_id = gameid
		self.hit = False

	def checkhit(self,x,y):
		if x==self.x and y==self.y:
			self.hit = True

class Request(db.Model):
	__tablename__ = 'Request'
	id = db.Column(db.Integer, primary_key=True)
	challenger = db.Column(db.Integer)
	receiver = db.Column(db.Integer)
	__table_args__ = (UniqueConstraint('challenger','receiver',name='ucr'),)

	def __init__(self,p1,p2):
		self.challenger = p1
		self.receiver = p2

	def __repr__(self):
		return '<Request %r %r>' % (self.challenger, self.receiver)



