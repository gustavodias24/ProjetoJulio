from pymongo import MongoClient
from flask import Flask, request, jsonify
from bson.objectid import ObjectId

mongo_uri = "mongodb+srv://julio:233281@cluster0.tq8708d.mongodb.net/"

client = MongoClient(mongo_uri)
db = client['db']
col_task = db['task']

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"msg": "Api funcionando"}), 200


@app.route("/create", methods=["POST"])
def createTask():
    body = request.get_json()
    if not body:
        return jsonify({"msg": "Corpo da requisição vazio!"}), 400

    col_task.insert_one(body)
    return jsonify({"msg": "Criado com sucesso!"}), 201


@app.route("/delete", methods=["DELETE"])
def deleteTask():
    id_task = request.args.get('id_task')
    if not id_task:
        return jsonify({"msg": "ID da tarefa não fornecido!"}), 400

    try:
        result = col_task.delete_one({"_id": ObjectId(id_task)})
        if result.deleted_count == 0:
            return jsonify({"msg": "Tarefa não encontrada!"}), 404
    except Exception as e:
        return jsonify({"msg": "Erro ao deletar a tarefa!", "error": str(e)}), 500

    return jsonify({"msg": "Deletado com sucesso!"}), 200


@app.route("/tasks", methods=["GET"])
def returnAllTasks():
    tasks = [x for x in col_task.find()]
    for task in tasks:
        task['_id'] = str(task['_id'])  # Convertendo ObjectId para string
    return jsonify(tasks), 200


if __name__ == "__main__":
    app.run(debug=True)
