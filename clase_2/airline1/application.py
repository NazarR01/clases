import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    query =  text("SELECT * FROM flights")
    flights = db.execute(query).fetchall()
    return render_template("index.html", flights=flights)

@app.route("/book", methods=["POST"])
def book():
    """Book a flight."""

    # Get form information.
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Invalid flight number.")

    # Make sure flight exists.
    query =  text("SELECT * FROM flights WHERE id = :id")
    if db.execute(query, {"id": flight_id}).rowcount == 0:
        return render_template("error.html", message="No such flight with that id.")
    query1 = text("INSERT INTO passengers (name, flight_id) VALUES (:name, :flight_id)")
    db.execute(query1,{"name": name, "flight_id": flight_id})
    db.commit()
    return render_template("success.html")

@app.route("/flights")
def flights():
    """Lists all flights."""
    query = text("SELECT * FROM flights")
    flights = db.execute(query).fetchall()
    return render_template("flights.html", flights=flights)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    """Lists details about a single flight."""

    # Make sure flight exists.
    query = text("SELECT * FROM flights WHERE id = :id")
    flight = db.execute(query, {"id": flight_id}).fetchone()
    if flight is None:
        return render_template("error.html", message="No such flight.")

    # Get all passengers.
    query1 = text("SELECT name FROM passengers WHERE flight_id = :flight_id")
    passengers = db.execute(query1,{"flight_id": flight_id}).fetchall()
    return render_template("flight.html", flight=flight, passengers=passengers)
