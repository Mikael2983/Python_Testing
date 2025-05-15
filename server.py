import json
from functools import wraps

from flask import Flask, render_template, request, redirect, flash, url_for, \
    session


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):

        club = session.get('club')
        if not club:
            flash("You must be logged in to access this page.")
            return redirect(url_for('index'))
        return view_func(*args, **kwargs)

    return wrapper


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    club = [club for club in clubs if club['email'] == request.form['email']]
    if club:
        session['club'] = club[0]
        return redirect(url_for('showSummary'))
    else:
        flash("Sorry, that email wasn't found.")

    return redirect(url_for('index'))


@app.route('/showSummary')
@login_required
def showSummary():
    club = session['club']
    return render_template('welcome.html',
                           club=club,
                           competitions=competitions)


@app.route('/book/<competition>/<club>')
@login_required
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',
                               club=foundClub,
                               competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
@login_required
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html',
                           club=club,
                           competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))