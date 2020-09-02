from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pprint as pp


app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:passwd123@192.168.0.11:5432/test"
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return "<User %r>" % self.name


db.create_all()

# TODO: creating first sample user
# db.session.add(Person(name="Old Mr. PotatoHead"))
# db.session.commit()

person = Person.query.first()


@app.route("/")
def index():
    return f"Hello, {person.name}!"


if __name__ == "__main__":
    app.run()
