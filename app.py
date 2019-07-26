from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
import os

app = Flask(__name__)
heroku = Heroku(app)

basedir= os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"]= "postgres://lkkgetbhmgolqx:f4cb5a99438eee0e6394cdf1fb3fb22b553b5bd351ce350a6e3a22d981dbf51a@ec2-54-235-92-43.compute-1.amazonaws.com:5432/dcq3jo2l305n3c"

CORS(app)#Make sure our app does not have errors
db= SQLAlchemy(app)
ma = Marshmallow(app)#wrapping our app to use modern methods


class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)#generated autommatically
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean)

    def __init__(self, title, done):
      self.title = title
      self.done = done

class TodoSchema(ma.Schema):
    class Meta:
        fields  = ("id","title","done")

todos_schema = TodoSchema(many=True) #instantiating class to have multiple objects
todo_schema = TodoSchema()#single record


@app.route("/todos", methods=["GET"])#uri: /todos to get all the items
def get_todos():
    all_todos = Todo.query.all()#selecting all the records
    result = todos_schema.dump(all_todos)#match each value into a key {:}

    return jsonify(result.data)

@app.route("/add-todo", methods=["POST"])
def add_todo():
    title = request.json["title"]
    done = request.json["done"]

    record = Todo(title,done)#instantitating class
    db.session.add(record)
    db.session.commit()
    todo = Todo.query.get(record.id)
    #getting record saved in the DB
    return todo_schema.jsonify(todo)

@app.route("/todo/<id>", methods=["PUT"])
def update_todo(id):
    todo= Todo.query.get(id)

    title = request.json["title"]
    done = request.json["done"]

    todo.title = title
    todo.done = done

    db.session.commit()
    #getting record saved in the DB
    return jsonify("UPDATE successful")

    

@app.route("/todo/<id>", methods=["DELETE"])
def delete_todo(id):
    record = Todo.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify("record deleted")





if __name__ == "__main__":
    app.debug = True
    app.run() #to run our app