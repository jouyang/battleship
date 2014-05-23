from flask import render_template,request,flash,redirect,url_for
from battleship import app,db
from models import *
from forms import *
from flask.ext.login import login_user, logout_user, current_user, login_required

@app.route('/')
@app.route('/index')
def index():
	if current_user.is_anonymous():
		user = None
		challenger_data = None
	else:
		user = current_user
		challenges = Request.query.filter_by(receiver=current_user.id)
		challengers_id = []
		challengers = []
		for c in challenges:
			challengers.append(User.query.get(c.challenger).username)
			challengers_id.append(c.challenger)
		challenger_data = zip(challengers_id,challengers)
	return render_template("index.html", user = user, challenger_data=challenger_data)

@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		# login and validate the user...
		user_name = form.username.data
		print user_name
		user = User.query.filter_by(username=user_name).first()
		if user is not None:
			if user.check_password(form.password.data):
				login_user(user)
				flash("Logged in successfully.")
				return redirect(url_for("index"))
			else:
				flash("Password Incorrect!")
		else:
			flash("User does not exist!")
	return render_template("login.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		check = User.query.filter_by(username = form.username.data).first()
		if check is None:
			user = User(form.username.data, form.email.data,form.password.data)
			db.session.add(user)
			db.session.commit()
			flash('Thanks for registering')
			return redirect(url_for('index'))
		else:
			error = 'Username taken!'
			return render_template('register.html', form=form,error=error)
	return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/list_game')
@login_required
def list_game():
	challenge_games = Game.query.filter_by(player1 = current_user.id).filter_by(ready=True)
	received_games = Game.query.filter_by(player2 = current_user.id).filter_by(ready=True)
	opponents = []
	challengers = []
	challenge_games_id = []
	received_games_id = []

	for g in challenge_games:
		opponents.append(User.query.get(g.player2).username)
		challenge_games_id.append(g.id)
	for g in received_games:
		challengers.append(User.query.get(g.player1).username)
		received_games_id.append(g.id)

	opponents_data = zip(opponents,challenge_games_id)
	challengers_data = zip(challengers,received_games_id)
	return render_template('list_game.html',  opponents_data= opponents_data, challengers_data= challengers_data,user = current_user)

@app.route('/challenge',methods=["GET", "POST"])
@login_required
def challenge():
	form = ChallengeForm(request.form)
	if request.method == 'POST' and form.validate():
		user_name = form.username.data
		user = User.query.filter_by(username=user_name).first()
		if user is not None:
			if (Game.query.filter_by(player1=current_user.id).filter_by(player2=user.id).first() or Game.query.filter_by(player2=current_user.id).filter_by(player1=user.id).first()) is not None:
				flash("There is already a challenge pending!")
				return redirect(url_for('challenge'))
			if Request.query.filter_by(challenger=current_user.id).filter_by(receiver=user.id).first() is not None:
				flash("A challenge has already been sent!")
				return redirect(url_for('challenge'))
			game = Game(current_user.id,user.id)
			db.session.add(game)
			db.session.commit()
			challenge = Request(current_user.id,user.id)
			db.session.add(challenge)
			db.session.commit()
			try:
				ship1 = Ships(form.ship1x.data,form.ship1y.data,int(current_user.id),game.id)
				ship2 = Ships(form.ship2x.data,form.ship2y.data,int(current_user.id),game.id)
				ship3 = Ships(form.ship3x.data,form.ship2y.data,int(current_user.id),game.id)
				db.session.add(ship1)
				db.session.add(ship2)
				db.session.add(ship3)
				db.session.commit()
				flash("Challenge Sent!")
				return redirect(url_for("index"))
			except:
				db.session.rollback()
				db.session.delete(game)
				db.session.delete(challenge)
				db.commit()
				flash("Duplicate ships!")
				return redirect(url_for("challenge"))
		else:
			flash("User does not exist!")
	return render_template("challenge.html", form=form)

@app.route('/accept/<c_id>')
@login_required
def accept(c_id):
	game = Game.query.filter_by(player1=c_id).filter_by(player2=current_user.id).first()
	return redirect(url_for('create_game',g_id=game.id))

@app.route('/game/<g_id>')
@login_required
def game(g_id):
	game = Game.query.get(g_id)
	if game.player1 != current_user.id and game.player2 != current_user.id:
		return redirect(url_for('index'))
	if game is None:
		flash("Game has ended!")
		return redirect(url_for('index'))
	opponent = None
	if game.player1 == current_user.id:
		opponent = User.query.get(game.player2)
	else:
		opponent = User.query.get(game.player1)
	opponent_moves = opponent.moves.filter_by(game_id=game.id)
	opponent_ships = opponent.ships.filter_by(game_id=game.id)
	player_moves = current_user.moves.filter_by(game_id=game.id)
	player_ships = current_user.ships.filter_by(game_id=game.id)

	return render_template("game.html",user=current_user,opponent=opponent,player_moves=player_moves,opponent_moves=opponent_moves,player_ships=player_ships,opponent_ships=opponent_ships)

@app.route('/create_game/<g_id>',methods=["GET", "POST"])
@login_required
def create_game(g_id):
	form = CreateGameForm(request.form)
	if request.method == 'POST' and form.validate():
		try:
			ship1 = Ships(form.ship1x.data,form.ship1y.data,int(current_user.id),g_id)
			ship2 = Ships(form.ship2x.data,form.ship2y.data,int(current_user.id),g_id)
			ship3 = Ships(form.ship3x.data,form.ship2y.data,int(current_user.id),g_id)
			db.session.add(ship1)
			db.session.add(ship2)
			db.session.add(ship3)
			db.session.commit()
			game = Game.query.get(g_id)
			game.set_ready()
			game.change_turn()
			db.session.commit()
			return redirect(url_for('list_game'))
		except:
			db.session.rollback()
			flash('Duplicate Ships!')
			return redirect(url_for('create_game',g_id=g_id))
	return render_template("create_game.html", form=form, g_id=g_id)




