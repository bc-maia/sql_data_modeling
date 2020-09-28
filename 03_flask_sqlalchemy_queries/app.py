from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
import pprint

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
        return f"<Person {self.id}: {self.name}>"


@app.route("/")
def index():
    if person := Person.query.first():
        return f"Hello, {person.name}!"
    else:
        return "Empty database"


# @app.route("/add_person", methods=["POST"])
# def add_person(parameter_list):
#     if request.method == "POST":
#         pp.pprint(parameter_list)


if __name__ == "__main__":
    app.run()
