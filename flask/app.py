from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pprint as pp


app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:passwd123@192.168.0.11:5432/test"
db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return "<User %r>" % self.name


db.create_all()


@app.route("/")
def index():
    if person := Person.query.first():
        return f"Hello, {person.name}!"
    else:
        return f"Empty database"


@app.route("/add_person")
def add_person():
    # TODO: creating first sample user
    db.session.add(Person(name="Old Mr. PotatoHead"))
    db.session.commit()
    return "person added"


@app.route("/delete_person")
def delete_person():
    if person := Person.query.first():
        db.session.delete(person)
        db.session.commit()
        return "person removed"
    else:
        return f"Empty database"


if __name__ == "__main__":
    app.run()
