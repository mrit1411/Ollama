from flask import Flask, Response, request, stream_with_context
import requests
import time
import threading

app = Flask(__name__)

# GLOBAL METRIC VARIABLES
total_requests = 0
request_timeouts = 0
total_delay = 0
delay_count = 0
active_users = 0
lock = threading.Lock()

OLLAMA_URL = "http://localhost:11434"  # Change if Ollama is elsewhere

@app.route("/api/generate", methods=["POST"])
def proxy_generate():
    global total_requests, request_timeouts, total_delay, delay_count, active_users

    with lock:
        active_users += 1

    start = time.time()
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            headers={"Content-Type": "application/json"},
            data=request.data,
            timeout=120,
            stream=True   # Key: stream Ollama's NDJSON
        )
        status = r.status_code

        # Stream response from Ollama directly to client
        def generate():
            for chunk in r.iter_content(chunk_size=None):
                if chunk:
                    yield chunk

        response_data = stream_with_context(generate())
        # Remove transfer-encoding header to let Flask set it
        headers = [(k, v) for k, v in r.headers.items() if k.lower() != 'transfer-encoding']

    except requests.Timeout:
        status = 504
        response_data = b"Timeout"
        headers = []
        with lock:
            request_timeouts += 1
    finally:
        duration = time.time() - start
        with lock:
            active_users -= 1

    with lock:
        total_requests += 1
        total_delay += duration
        delay_count += 1

    return Response(response_data, status=status, headers=dict(headers))

@app.route("/metrics")
def metrics():
    with lock:
        avg_delay = (total_delay / delay_count) if delay_count > 0 else 0
        metrics_text = f"""
ollama_requests_total {total_requests}
ollama_request_timeouts {request_timeouts}
ollama_avg_delay_seconds {avg_delay:.3f}
ollama_active_users {active_users}
"""
    return Response(metrics_text, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
