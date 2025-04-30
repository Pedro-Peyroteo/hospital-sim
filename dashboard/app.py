from flask import Flask, jsonify
from server.state import triage_queue
from event_listener import messages, listen_to_hospital_broadcast, threads_info

app = Flask(__name__)

@app.route("/queue")
def get_queue():
    try:
        items = []
        temp_queue = []
        
        while not triage_queue.empty():
            item = triage_queue.get()
            temp_queue.append(item)
            items.append({"pid": item.pid, "urgency": item.urgency})
            
        for item in temp_queue:
            triage_queue.put(item)
        
        return jsonify(items)
        
    except Exception as e:
        return jsonify({"error": str(e)}),500
    
@app.route("/threads")
def get_threads():
    return jsonify(threads_info or {"error": "No thread info received yet."})

@app.route("/events")
def get_events():
    return jsonify(messages[-20:])

@app.route("/")
def home():
    return jsonify({"message": "Hospital Dashboard API running"})


if __name__ == "__main__":
    listen_to_hospital_broadcast()
    app.run(host="0.0.0.0", port=8000)