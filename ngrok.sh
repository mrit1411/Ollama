#!/bin/bash
echo "[*] Starting ngrok tunnel on port 8005 (forwarded from svc/ollama-service)..."

# Run port-forward in the background
kubectl port-forward svc/ollama-service 8005:8000 &
PF_PID=$!

# Start ngrok tunnel
ngrok http 8005

# Kill port-forward if ngrok stops
kill $PF_PID
