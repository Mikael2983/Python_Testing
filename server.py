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


def has_enough_points(club: dict, requested: int) -> bool:
    """check if the club has enough points to book the requested places """
    return int(club['points']) >= requested


def has_enough_places_available(competition: dict, placesRequired: int) -> bool:
    """Check that the competition has more places available than requested"""
    return int(competition['numberOfPlaces']) > placesRequired


def is_booking_limit_exceeded(club_name: str, competition: dict,
                              requested: int) -> bool:
    """ check if the club is trying to book more than 12 places """
    bookedPlaces = int(competition.get("bookings", {}).get(club_name, 0))
    return bookedPlaces + requested > 12


def update_booking(club: dict, competition: dict, requested: int) -> None:
    """
    updates the club and competition after a booking,
    creates the dictionary "booking" for the competition if it doesn't exist
    """
    club['points'] = str(int(club['points']) - requested)
    competition['numberOfPlaces'] = str(
        int(competition['numberOfPlaces']) - requested)

    if "bookings" not in competition:
        competition["bookings"] = {}

    bookedPlaces = int(competition["bookings"].get(club['name'], 0))
    competition["bookings"][club['name']] = str(bookedPlaces + requested)


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
    club_name = session.get('club')['name']
    club = next(c for c in clubs if c['name'] == club_name)

    competition = next(c for c in competitions
                       if c['name'] == request.form['competition'])

    placesRequired = int(request.form['places'])

    if is_booking_limit_exceeded(club['name'], competition, placesRequired):
        flash("you can't book more than 12 places.")
    elif not has_enough_points(club, placesRequired):
        flash("you don't have enough points")
    elif not has_enough_places_available(competition, placesRequired):
        flash("there are not enough places available")
    else:
        update_booking(club, competition, placesRequired)
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