import requests
import time
import random

API_SERVER = "http://host.docker.internal:5000"
NODE_ID = "Node1"

def register_node():
    data = {
        "node_id": NODE_ID,
        "cpu_limit": 50
    }
    try:
        res = requests.post(f"{API_SERVER}/register_node", json=data)
        print(res.json())
    except Exception as e:
        print(f"Registration failed: {e}")

def send_heartbeat():
    while True:
        cpu_usage = random.randint(10, 70)
        data = {
            "node_id": NODE_ID,
            "cpu_usage": cpu_usage
        }
        try:
            res = requests.post(f"{API_SERVER}/update_cpu_usage", json=data)
            print(res.json())
        except Exception as e:
            print(f"Heartbeat failed: {e}")
        time.sleep(5)

if __name__ == "__main__":
    register_node()
    send_heartbeat()
