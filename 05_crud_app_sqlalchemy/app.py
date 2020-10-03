import json
import sys
from flask import Flask, request, render_template, jsonify, abort

# from flask import redirect, url_for
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