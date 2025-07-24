#!/bin/bash

echo "🚀 Starting Ollama port-forward + Ngrok tunnel..."

# Step 1: Start minikube tunnel in a new Git Bash terminal window
echo "🔁 Starting minikube tunnel in new terminal..."
start "" "C:\Program Files\Git\git-bash.exe" -c "minikube tunnel"

# Step 2: Port-forward Ollama service
echo "🌐 Port-forwarding Ollama service on localhost:11435..."
fuser -k 11435/tcp 2>/dev/null || true
kubectl port-forward svc/ollama-service 11435:11434 > /dev/null 2>&1 &

# Step 3: Start Ngrok
echo "🔗 Launching Ngrok on port 11435..."
ngrok http 11435
