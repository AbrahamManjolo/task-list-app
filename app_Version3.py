from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample task data
tasks = [
    {"id": 1, "title": "Finish assignment", "priority": "high", "dueDate": "", "completed": False},
    {"id": 2, "title": "Buy groceries", "priority": "low", "dueDate": "", "completed": False},
    {"id": 3, "title": "Study for exam", "priority": "high", "dueDate": "", "completed": False},
    {"id": 4, "title": "Clean room", "priority": "medium", "dueDate": "", "completed": False}
]

task_id_counter = 5

@app.route("/tasks", methods=["GET"])
def get_tasks():
    search = request.args.get("search", "").lower()
    priority = request.args.get("priority", "").lower()

    filtered_tasks = tasks

    # Search filter
    if search:
        filtered_tasks = [
            task for task in filtered_tasks
            if search in task["title"].lower()
        ]

    # Priority filter
    if priority:
        filtered_tasks = [
            task for task in filtered_tasks
            if task["priority"].lower() == priority
        ]

    return jsonify(filtered_tasks), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id_counter
    data = request.json
    
    new_task = {
        "id": task_id_counter,
        "title": data.get("text", ""),
        "dueDate": data.get("dueDate", ""),
        "priority": data.get("priority", "medium"),
        "completed": False
    }
    
    tasks.append(new_task)
    task_id_counter += 1
    
    return jsonify(new_task), 201


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"message": "Task deleted"}), 200


@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.json
    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    if "completed" in data:
        task["completed"] = data["completed"]
    
    return jsonify(task), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)