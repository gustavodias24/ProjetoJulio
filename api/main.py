from pymongo import MongoClient
from flask import Flask, request, jsonify

mongo_uri = "mongodb+srv://julio:233281@cluster0.tq8708d.mongodb.net/"

client = MongoClient(mongo_uri)
db = client['db']
col_task = db['task']

app = Flask(__name__)


@app.route("/create")
def createTask():
    body = request.get_json()

    col_task.insert_one(body)

    return jsonify({"msg": "Criado com sucesso!"}), 201


@app.route("/delete", methods=["DELETE"])
def deleteTask():
    id_task = request.args.get('id_task')
    col_task.delete_one({"_id": id_task})

    return jsonify({"msg": "Deletado com sucesso!"}), 200


@app.route("/tasks")
def returnAllTasks():
    return [x for x in col_task.find()]


if __name__ == "__main__":
    app.run()
