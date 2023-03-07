import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():

    # List all flights.
    query = text("SELECT id, origin, destination, duration FROM flights")
    flights = db.execute(query).fetchall()
    for flight in flights:
        print(f"Flight {flight.id}: {flight.origin} to {flight.destination}, {flight.duration} minutes.")

    # Prompt user to choose a flight.
    flight_id = int(input("\nFlight ID: "))
    query1 = text("SELECT origin, destination, duration FROM flights WHERE id = :id")
    flight = db.execute(query1, {"id": flight_id}).fetchone()

    # Make sure flight is valid.
    if flight is None:
        print("Error: No such flight.")
        return

    # List passengers.
    query2 = text("SELECT name FROM passengers WHERE flight_id = :flight_id")
    passengers = db.execute(query2,{"flight_id": flight_id}).fetchall()
    print("\nPassengers:")
    for passenger in passengers:
        print(passenger.name)
    if len(passengers) == 0:
        print("No passengers.")

if __name__ == "__main__":
    main()
