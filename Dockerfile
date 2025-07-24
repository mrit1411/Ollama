FROM ollama/ollama

# Install deps if needed
RUN apt-get update && apt-get install -y curl gnupg && apt-get clean

# Start ollama, pull the model, then shut it down
RUN ollama serve & \
    sleep 15 && \
    ollama pull gemma:2b && \
    pkill ollama

# Use your own entrypoint if needed
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
