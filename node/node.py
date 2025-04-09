import requests
import time
import os

API_SERVER = "http://api_server:5050"
NODE_ID = os.getenv("NODE_ID", "node-1")
CPU_CORES = os.getenv("CPU_CORES", "2")

def register_node():
    response = requests.post(f"{API_SERVER}/register_node", json={"node_id": NODE_ID, "cpu_limit": CPU_CORES})
    print(response.json())

def send_heartbeat():
    while True:
        try:
            requests.post(f"{API_SERVER}/heartbeat", json={"node_id": NODE_ID})
            print(f"Heartbeat sent from {NODE_ID}")
        except Exception as e:
            print(f"Error sending heartbeat: {e}")
        time.sleep(5)

if __name__ == "__main__":
    register_node()
    send_heartbeat()

   

