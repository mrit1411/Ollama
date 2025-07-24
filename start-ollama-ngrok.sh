#!/bin/bash

echo "🚀 Starting Ollama port-forward + Ngrok tunnel..."

# Step 1: Start minikube tunnel in a new Git Bash terminal window
echo "🔁 Starting minikube tunnel in new terminal..."
start "" "C:\Program Files\Git\git-bash.exe" -c "minikube tunnel"
