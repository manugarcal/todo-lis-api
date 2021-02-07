from flask import Flask, render_template, jsonify, request
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, Todo
import json


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True 
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Chetifrega@localhost:3306/todolistapi' 
db.init_app(app)
Migrate(app, db)
CORS(app)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/todos/user/<username>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def todos(username):
    if request.method == 'GET':
        todo = Todo.query.filter_by(username=username).first()
        if not todo:
            return jsonify({"msg": "User not found"})

        return jsonify(todo.serialize()), 200

    if request.method == 'POST':
        #get a request body
        body = request.get_json()
        #validate the data type must be a list
        if  type(body) is not list:
            return jsonify({"msg": "Not Found"}), 404
        #add an default object
        body.append({"label": "Default Task", "done": "false"})
        #create a new class todo instance
        todo = Todo()
        #assing a username
        todo.username = username
        #convert todo list to string
        todo.tasks = json.dumps(body)
        #save in DB
        todo.save()

        return jsonify({"Result": "ok"}), 201

    if request.method == 'PUT':
        body = request.get_json()
        todo = Todo.query.filter_by(username=username).first()
        if todo:
            todo.tasks = json.dumps(body)
            todo.update()
            return jsonify({"msg": "a list whit " + str(len(body)) + " todos was successfully saved" }), 200
        else:
            return jsonify({"msg": "User not found"}), 404
    if request.method == 'DELETE':
        todo = Todo.query.filter_by(username=username).first()
        if todo:
            todo.delete()
            return jsonify({"result": "ok"}), 200
        else:
            return jsonify({"msg": "User not Found"}), 404

        

if __name__ == '__main__':
    manager.run()