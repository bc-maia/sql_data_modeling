import json
import sys
from flask import Flask, request, render_template, jsonify, abort
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:passwd123@localhost:5432/todoapp"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<To-Do ID: {self.id}, Description: {self.description}, Status: {self.completed}>"


@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", context=todos)


@app.route("/api/todo", methods=["GET", "POST"])
def api_todo():
    if request.method == "GET":
        todos = Todo.query.all()
        response = {i: {"Description": t.description} for i, t in enumerate(todos)}
        return jsonify(response)

    if request.method == "POST":
        if request.data:
            if description := request.get_json()["description"]:
                response = {}
                try:
                    todo = Todo(description=description)
                    db.session.add(todo)
                    db.session.commit()
                    response["description"] = description
                except:
                    db.session.rollback()
                    print(sys.exc_info())
                    response = None
                finally:
                    db.session.close()

                return jsonify(response) if response else abort(500)
        abort(400)


if __name__ == "__main__":
    app.run()
