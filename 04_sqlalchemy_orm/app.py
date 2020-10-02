import json
from flask import Flask
from flask import request
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:passwd123@localhost:5432/test"

db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"<Person ID:{self.id}, Name: {self.name}>"


# this must be after a db.Model class declaration
db.create_all()


@app.route("/")
def index():
    if person := Person.query.first():
        response = f"Hello, {person.name}!"
        status = 200
    else:
        response = "Empty database"
        status = 302

    return Response(response=response, status=status)


@app.route("/add_person", methods=["POST"])
def add_person():
    if request.method == "POST":
        payload = json.loads(request.data)
        if name := payload["name"]:
            db.session.add(Person(name=name))
            db.session.commit()
        return Response(status=200)


@app.route("/people")
def show_people():
    if people := Person.query.all():
        response = [(x.id, x.name) for x in people]
        return Response(status=200, response=json.dumps(response))
    return Response(status=404)


if __name__ == "__main__":
    app.run()
