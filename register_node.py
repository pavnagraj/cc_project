import requests

response = requests.post("http://127.0.0.1:5050/register_node", json={
    "node_id": "Node1",
    "cpu_limit": 50
})

print(response.text)
