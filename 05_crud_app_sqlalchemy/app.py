import json
from flask import Flask, request, render_template
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy


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


@app.route("/")
def index():
    return render_template("index.html", context=Todo.query.all())


@app.route("/todo/create", methods=["POST"])
def create():
    if request.method == "POST":
        if description := request.form.get("description"):
            store_todo(description)

        return render_template("index.html", context=Todo.query.all())


@app.route("/api/todo", methods=["GET"])
def api_list():
    todos = Todo.query.all()
    response = {t.id: {"Description": t.description} for t in todos}
    return response


@app.route("/api/todo", methods=["POST"])
def api_create():
    if request.method == "POST":
        data = json.loads(request.data)
        if description := data.get("description"):
            todo = store_todo(description)
            return f"Task {todo} created"


def store_todo(description: str) -> Todo:
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    return todo


if __name__ == "__main__":
    app.run()