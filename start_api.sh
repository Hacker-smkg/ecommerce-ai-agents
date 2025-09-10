#!/bin/bash

echo "Starting E-commerce AI Agents API Server..."
echo "API will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "Press Ctrl+C to stop the API server"

# Start FastAPI server
python api_server.py
