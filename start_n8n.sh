#!/bin/bash

# Set n8n data directory
export N8N_USER_FOLDER="./n8n_workflows"

# Create necessary directories
mkdir -p ./n8n_workflows

echo "Starting n8n for E-commerce AI Agents..."
echo "n8n will be available at: http://localhost:5678"
echo "Press Ctrl+C to stop n8n"

# Start n8n
n8n start
