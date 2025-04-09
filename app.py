from flask import Flask, request, jsonify

app = Flask(__name__)

# Store node info
registered_nodes = []

@app.route('/register_node', methods=['POST'])
def register_node():
    data = request.get_json()
    print("Received registration:", data)
    registered_nodes.append(data)
    return jsonify({"message": "Node registered successfully"}), 200

@app.route('/update_cpu_usage', methods=['POST'])
def update_cpu():
    data = request.get_json()
    print("Received CPU update:", data)
    return jsonify({"message": "CPU usage updated"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
