from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample task data
tasks = [
    {"id": 1, "title": "Finish assignment", "priority": "high"},
    {"id": 2, "title": "Buy groceries", "priority": "low"},
    {"id": 3, "title": "Study for exam", "priority": "high"},
    {"id": 4, "title": "Clean room", "priority": "medium"}
]

@app.route("/tasks", methods=["GET"])
def get_tasks():
    search = request.args.get("search")
    priority = request.args.get("priority")

    filtered_tasks = tasks

    # Search filter
    if search:
        filtered_tasks = [
            task for task in filtered_tasks
            if search.lower() in task["title"].lower()
        ]

    # Priority filter
    if priority:
        filtered_tasks = [
            task for task in filtered_tasks
            if task["priority"].lower() == priority.lower()
        ]

    return jsonify(filtered_tasks), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)