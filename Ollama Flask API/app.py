
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
OLLAMA = "http://localhost:11434"
MODEL = "llama3.2:1b"


# Send a request to the Ollama API endpoint and return the JSON response.
def ask(endpoint, data=None):
    r = requests.post(f"{OLLAMA}{endpoint}", json=data, timeout=300) if data else requests.get(f"{OLLAMA}{endpoint}", timeout=10)
    r.raise_for_status()
    return r.json()


# Return a simple welcome message for the root route.
@app.get("/")
def home():
    return jsonify(message="Ollama API is running")


# Check whether the Ollama service is reachable and healthy.
@app.get("/health")
@app.get("/status")
def health():
    try:
        ask("/api/tags")
        return jsonify(status="connected")
    except requests.RequestException:
        return jsonify(status="disconnected"), 503


# Return the list of available Ollama models.
@app.get("/models")
def models():
    try:
        return jsonify(ask("/api/tags"))
    except requests.RequestException:
        return jsonify(error="Ollama unavailable"), 502


# Generate a text response from the configured model using a single prompt.
@app.post("/generate")
def generate():
    prompt = (request.json or {}).get("prompt", "")
    if not prompt.strip():
        return jsonify(error="Prompt required"), 400

    try:
        return jsonify(response=ask("/api/generate", {
            "model": MODEL, "prompt": prompt, "stream": False
        })["response"])
    except (requests.RequestException, KeyError):
        return jsonify(error="Generation failed"), 502


# Generate a chat response using a list of message objects.
@app.post("/chat")
def chat():
    messages = (request.json or {}).get("messages", [])
    if not isinstance(messages, list) or not messages:
        return jsonify(error="Messages required"), 400

    try:
        return jsonify(response=ask("/api/chat", {
            "model": MODEL, "messages": messages, "stream": False
        })["message"]["content"])
    except (requests.RequestException, KeyError):
        return jsonify(error="Chat failed"), 502


# Run the Flask app on port 5000 when this file is executed directly.
if __name__ == "__main__":
    app.run(port=5000)
