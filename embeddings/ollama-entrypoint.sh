#!/bin/sh

echo "Start ollama server"

# Execute the original entrypoint command in the background
ollama serve &

# Capture the process ID of the background job
ollama_serve_pid=$!

sleep 10

# Pull the model from ollama index
echo "Pull $OLLAMA_MODEL model"
ollama pull $OLLAMA_MODEL &

# Capture the process ID of the pull job
ollama_pull_pid=$!

# Wait for the pull job to complete
wait $ollama_pull_pid
echo "Model pulled"

echo "Ollama server started"

# Bring the serve job back to the foreground
wait $ollama_serve_pid
