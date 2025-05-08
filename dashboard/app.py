from flask import Flask, jsonify
from server.state import triage_queue
from event_listener import messages, listen_to_hospital_broadcast, threads_info

app = Flask(__name__)

@app.route("/queue")
def get_queue():
    try:
        items = [
            {
                "pid": patient.pid,
                "name": patient.name,
                "age": patient.age,
                "urgency": patient.urgency,
                "symptoms": patient.symptoms
            }
            for patient in list(triage_queue.queue)
        ]

        return jsonify(items)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/threads")
def get_threads():
    if threads_info:
        return jsonify({
            "active_count": threads_info.get("active", 0),
            "timestamp": threads_info.get("timestamp"),
            "thread_names": threads_info.get("threads", [])
        })
    return jsonify({"error": "No thread info received yet."})

@app.route("/events")
def get_events():
    return jsonify(messages[-20:])

@app.route("/")
def home():
    return jsonify({"message": "Hospital Dashboard API running"})


if __name__ == "__main__":
    listen_to_hospital_broadcast()
    app.run(host="0.0.0.0", port=8000)