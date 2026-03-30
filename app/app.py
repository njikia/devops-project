from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "taskdb"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "postgres")
    )

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, done FROM tasks")
    tasks = [{"id": r[0], "title": r[1], "done": r[2]} for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id",
                (data["title"], False))
    task_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": task_id, "title": data["title"], "done": False}), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def complete_task(task_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET done = TRUE WHERE id = %s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Task completed"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


    