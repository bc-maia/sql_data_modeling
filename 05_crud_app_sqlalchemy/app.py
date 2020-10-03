import json
from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect


app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:passwd123@localhost:5432/todoapp"
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<To-Do ID: {self.id}, Description: {self.description}>"


db.create_all()


# TODO: only used via form post
# @app.route("/todo/create", methods=["POST"])
# def create():
#     if request.method == "POST":
#         if description := request.form.get("description"):
#             store_todo(description)
#     return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("index.html", context=Todo.query.all())


@app.route("/api/todo", methods=["GET", "POST"])
def api_todo():
    if request.method == "GET":
        todos = Todo.query.all()
        response = {t.id: {"Description": t.description} for t in todos}
        return response

    if request.method == "POST":
        if request.data:
            if description := request.get_json()["description"]:
                todo = store_todo(description)
                return jsonify({"description": todo.description})

        return Response(status=400, response="Must send a payload")


def store_todo(description: str) -> Todo:
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    return todo


if __name__ == "__main__":
    app.run()