import json
import sys
from flask import Flask, request, render_template, jsonify, abort
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import backref
from werkzeug.utils import redirect

# Config
app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:passwd123@localhost:5432/todoapp"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Models
class TodoList(db.Model):
    __tablename__ = "todolists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship("Todo", backref="list", lazy=True)

    def __repr__(self):
        return f"<To-Do List ID: {self.id}, Name: {self.name}, To Do's: {self.todos}>"


class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey("todolists.id"), nullable=False)

    def __repr__(self):
        return f"<To-Do ID: {self.id}, Description: {self.description}, Status: {self.completed}>"


# routes
@app.route("/api/todo", methods=["GET"])
def api_todo():
    todos = Todo.query.all()
    response = {
        t.id: {"Description": t.description, "Completed": t.completed} for t in todos
    }
    return jsonify(response)


@app.route("/api/todo", methods=["POST"])
def api_todo_new():
    if request.method == "POST":
        if request.data:
            if description := request.get_json()["description"]:
                response = {}
                try:
                    todo = Todo(description=description)
                    db.session.add(todo)
                    db.session.commit()
                    response["description"] = description
                    response["id"] = todo.id
                except:
                    db.session.rollback()
                    print(sys.exc_info())
                    response = None
                finally:
                    db.session.close()

                return jsonify(response) if response else abort(500)
        abort(400)


@app.route("/api/todo/<todo_id>", methods=["POST", "DELETE"])
def api_todo_update(todo_id):
    if request.method == "POST":
        try:
            completed = request.get_json()["completed"]
            todo = Todo.query.get(todo_id)
            todo.completed = completed
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

        return redirect(url_for("index"))

    if request.method == "DELETE":
        success = False
        try:
            todo = Todo.query.get(todo_id)
            db.session.delete(todo)
            db.session.commit()
            success = True
        except:
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

        return jsonify({"success": success}) if success else abort(400)


@app.route("/api/lists/<list_id>")
def get_list_todos(list_id):
    todos = Todo.query.filter_by(list_id=list_id).order_by("id").all()
    return render_template("index.html", context=todos)


@app.route("/")
def index():
    return redirect(url_for("get_list_todos", list_id=1))


if __name__ == "__main__":
    app.run()
