import json
import sys
from flask import Flask, request, render_template, jsonify, abort
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import backref
from werkzeug.utils import redirect

# CONFIG
app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:passwd123@localhost:5432/todoapp"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)


# MODELS
class TodoList(db.Model):
    __tablename__ = "todolists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship("Todo", backref="list", lazy=True)

    def __repr__(self):
        return f"<TodoList ID: {self.id}, name: {self.name}, todos: {self.todos}>"


class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    complete = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey("todolists.id"), nullable=False)

    def __repr__(self):
        return f"<Todo ID: {self.id}, description: {self.description}, complete: {self.complete}>"


# ROUTES
@app.route("/api/list", methods=["GET"])
def api_list():
    todo_lists = TodoList.query.all()
    response = {t.id: {"Name": t.name} for t in todo_lists}
    return jsonify(response)


@app.route("/api/list", methods=["POST"])
def api_list_create():
    if request.method == "POST":
        if request.data:
            if name := request.get_json()["name"]:
                response = {}
                try:
                    list = TodoList(name=name)
                    db.session.add(list)
                    db.session.commit()
                    response["id"] = list.id
                    response["name"] = list.name
                except:
                    db.session.rollback()
                    print(sys.exc_info())
                    response = None
                finally:
                    db.session.close()

                return jsonify(response) if response else abort(500)
        abort(400)


@app.route("/api/list/<list_id>", methods=["POST"])
def api_list_update(list_id):
    error = False
    try:
        list = TodoList.query.get(list_id)
        for todo in list.todos:
            todo.complete = True
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return "", 200


@app.route("/api/list/<list_id>", methods=["DELETE"])
def api_list_delete(list_id):
    success = False
    try:
        list = TodoList.query.get(list_id)
        for todo in list.todos:
            db.session.delete(todo)
        db.session.delete(list)
        db.session.commit()
        success = True
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    return jsonify({"success": success}) if success else abort(400)


@app.route("/api/todo", methods=["GET"])
def api_todo():
    todos = Todo.query.all()
    response = {
        t.id: {"Description": t.description, "complete": t.complete} for t in todos
    }
    return jsonify(response)


@app.route("/api/todo", methods=["POST"])
def api_todo_new():
    if request.data:
        description = request.get_json()["description"]
        list_id = request.get_json()["list_id"]
        if description and list_id:
            response = {}
            try:
                todo = Todo(description=description, complete=False, list_id=list_id)
                db.session.add(todo)
                db.session.commit()
                response["id"] = todo.id
                response["description"] = todo.description
                response["complete"] = todo.complete
            except:
                db.session.rollback()
                print(sys.exc_info())
                response = None
            finally:
                db.session.close()

            return jsonify(response) if response else abort(500)
    abort(400)


@app.route("/api/todo/<todo_id>", methods=["POST"])
def api_todo_update(todo_id):
    try:
        complete = request.get_json()["complete"]
        todo = Todo.query.get(todo_id)
        todo.complete = complete
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    return redirect(url_for("index"))


@app.route("/api/todo/<todo_id>", methods=["DELETE"])
def api_todo_delete(todo_id):
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
def api_list_todos(list_id):
    if todo_list := TodoList.query.get(list_id):
        active_list = todo_list.name
        lists = TodoList.query.all()
        todos = Todo.query.filter_by(list_id=list_id).order_by("id").all()

        return render_template(
            "index.html", lists=lists, active_list=active_list, todos=todos
        )
    else:
        return redirect(url_for("api_list_todos", list_id=1))


@app.route("/")
def index():
    return redirect(url_for("api_list_todos", list_id=1))


if __name__ == "__main__":
    app.run(debug=True)
