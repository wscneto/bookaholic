import sys, os, requests
from flask import Flask, request, jsonify
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)

SERVICES = {
    'user': 'http://localhost:5001',
    'catalog': 'http://localhost:5002',
    'order': 'http://localhost:5003',
    'review': 'http://localhost:5004',
    'recommendation': 'http://localhost:5005',
}

def proxy(service, path):
    url = f"{SERVICES[service]}/{path}"
    resp = requests.request(
        method=request.method,
        url=url,
        headers={k: v for k, v in request.headers if k != 'Host'},
        params=request.args,
        json=request.get_json(silent=True)
    )
    return (resp.content, resp.status_code, resp.headers.items())

@app.route('/', methods=['GET'])
def index():
    return jsonify({"service": "api_gateway", "status": "running"})

@app.route('/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def route_to_service(service, path):
    if service not in SERVICES:
        return "Service not found", 404
    return proxy(service, path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)