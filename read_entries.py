from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import RSVP, Base

# Connect to the SQLite database
engine = create_engine('sqlite:///app/test.db')
Session = sessionmaker(bind=engine)


def get_db_entries():
    session = Session()
    try:
        # Query the RSVP table
        rsvps = session.query(RSVP).all()

        # Print the results
        for rsvp in rsvps:
            print(
                f"Name: {rsvp.name}, Email: {rsvp.email}, Attending: {rsvp.attending}, Bringing Food: {rsvp.bringing_food}, Bringing Drink: {rsvp.bringing_drink}, Message: {rsvp.message}")
    finally:
        # Close the session
        session.close()


if __name__ == "__main__":
    get_db_entries()
