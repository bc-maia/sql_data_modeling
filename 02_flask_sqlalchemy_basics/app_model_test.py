from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pprint as pp


app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:passwd123@localhost:5432/testingdatabase"
db = SQLAlchemy(app)


class Drivers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, unique=True, nullable=False)


db.session.add(Drivers(first_name="Old Mr.", last_name="PotatoHead"))
db.session.commit()
drivers = Drivers.query.all()
for driver in drivers:
    pp.pprint(driver.last_name)

potatoes = Drivers.query.filter_by(last_name="PotatoHead").all()
for potato in potatoes:
    db.session.delete(potato)

db.session.commit()

drivers = Drivers.query.all()


@app.route("/")
def index():
    drivers = Drivers.query.all()
    pp.pprint(drivers)
    return f"drivers found: {len(drivers)}"


# class Vehicle(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     driver_id = db.Column(db.Integer, primary_key=True)
#     make = db.Column(db.String, nullable=False)
#     model = db.Column(db.String, unique=True, nullable=False)


if __name__ == "__main__":
    app.run()
