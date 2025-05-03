import subprocess, os, signal, sys

services = {
    "api_gateway": 5000,
    "user_service": 5001,
    "catalog_service": 5002,
    "order_service": 5003,
    "review_service": 5004,
    "recommendation_service": 5005,
}

processes = []

def start_service(name, port):
    path = os.path.join(os.getcwd(), name)
    venv_python = os.path.join(os.getcwd(), '.venv', 'bin', 'python')
    if not os.path.exists(venv_python):
        venv_python = 'python'

    print(f"Starting {name} on port {port}...")
    proc = subprocess.Popen(
        [venv_python, 'app.py'],
        cwd=path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    processes.append(proc)

def stop_services():
    print("\nStopping services...")
    for proc in processes:
        try:
            proc.terminate()
        except Exception:
            pass

if __name__ == '__main__':
    try:
        for name, port in services.items():
            start_service(name, port)

        print("All services started. Press Ctrl+C to stop.")
        while True:
            pass

    except KeyboardInterrupt:
        stop_services()
        sys.exit(0)
