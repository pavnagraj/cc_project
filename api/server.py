from flask import Flask, request, jsonify
from datetime import datetime
import threading
import time

app = Flask(__name__)

# Unified state for nodes and pods
cluster_state = {
    "nodes": {},
    "pods": {},
    "pod_counter": 1
}

@app.route('/register_node', methods=['POST'])
def register_node():
    data = request.get_json()

    if "node_id" not in data or "cpu_limit" not in data:
        return jsonify({"error": "Missing node_id or cpu_limit"}), 400

    node_id = data["node_id"]
    cpu_limit = data["cpu_limit"]

    cluster_state["nodes"][node_id] = {
        "cpu_limit": cpu_limit,
        "cpu_usage": 0,
        "pods": [],
        "last_heartbeat": datetime.utcnow().timestamp(),
        "health": "healthy"
    }

    return jsonify({"message": f"Node {node_id} registered with CPU limit {cpu_limit}!"})

@app.route('/get_nodes', methods=['GET'])
def get_nodes():
    return jsonify(cluster_state["nodes"])

@app.route('/update_cpu_usage', methods=['POST'])
def update_cpu_usage():
    data = request.get_json()

    node_id = data.get("node_id")
    cpu_usage = data.get("cpu_usage")

    if node_id not in cluster_state["nodes"]:
        return jsonify({"error": "Node not found"}), 404

    # ✅ Update CPU usage
    cluster_state["nodes"][node_id]["cpu_usage"] = cpu_usage

    # ✅ Update heartbeat timestamp here as well
    cluster_state["nodes"][node_id]["last_heartbeat"] = datetime.utcnow().timestamp()

    if cpu_usage > cluster_state["nodes"][node_id]["cpu_limit"]:
        return jsonify({"warning": f"Node {node_id} exceeded CPU limit!"})

    return jsonify({"message": f"CPU usage for {node_id} updated to {cpu_usage}"}), 200

@app.route('/launch_pod', methods=["POST"])
def launch_pod():
    data = request.get_json()

    try:
        cpu_request = int(data.get("cpu_request"))
    except (TypeError, ValueError):
        return jsonify({"error": "cpu_request must be an integer"}), 400

    pod_id = f"pod{cluster_state['pod_counter']}"

    for node_id, node_info in cluster_state["nodes"].items():
        if node_info.get("health") != "healthy":
            continue

        available_cpu = int(node_info["cpu_limit"]) - node_info["cpu_usage"]
        if available_cpu >= cpu_request:
            node_info["cpu_usage"] += cpu_request
            node_info["pods"].append(pod_id)

            cluster_state["pods"][pod_id] = {
                "cpu": cpu_request,
                "node": node_id
            }

            cluster_state["pod_counter"] += 1

            return jsonify({
                "message": f"{pod_id} launched on {node_id}",
                "assigned_node": node_id
            }), 200

    return jsonify({"error": "No healthy node has enough CPU resources"}), 503

@app.route('/cluster_status', methods=["GET"])
def cluster_status():
    current_time = datetime.utcnow().timestamp()
    status = {}

    for node_id, node_info in cluster_state["nodes"].items():
        last = node_info.get("last_heartbeat", 0)
        is_alive = (current_time - last) < 10
        status[node_id] = {
            "cpu_limit": node_info["cpu_limit"],
            "cpu_usage": node_info["cpu_usage"],
            "status": "alive" if is_alive else "dead",
            "last_heartbeat": last
        }

    return jsonify(status)

@app.route('/heartbeat', methods=["POST"])
def heartbeat():
    data = request.get_json()
    node_id = data.get("node_id")

    if node_id not in cluster_state["nodes"]:
        return jsonify({"error": "Node not found"}), 404

    cluster_state["nodes"][node_id]["last_heartbeat"] = datetime.utcnow().timestamp()
    return jsonify({"message": f"Heartbeat received from {node_id}"})

def monitor_heartbeats():
    while True:
        now = datetime.utcnow().timestamp()
        for node_id, node_info in cluster_state["nodes"].items():
            last = node_info.get("last_heartbeat", 0)
            if now - last > 10:
                node_info["health"] = "unhealthy"
            else:
                node_info["health"] = "healthy"
        time.sleep(5)

# ✅ Start heartbeat monitor in background
heartbeat_thread = threading.Thread(target=monitor_heartbeats, daemon=True)
heartbeat_thread.start()

if __name__ == '__main__':
    print("API server running on port 5050...")
    app.run(host='0.0.0.0', port=5050, debug=True)

