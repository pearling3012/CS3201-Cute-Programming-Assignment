# Makefile for TodoTracker

# Python interpreter
PYTHON = python3

# Files
SERVER = TodoTrackerServer.py
CLIENT = TodoTrackerClient.py

# Default server IP and port
SERVER_IP = 127.0.0.1
SERVER_PORT = 18222

# Default target: show help
all: help

# Show help message
help:
	@echo "TodoTracker Makefile Commands:"
	@echo "  make server          - Start the server on port 18222"
	@echo "  make client          - Start the client (will prompt for IP/port)"
	@echo "  make client-test     - Start the client with default IP/port (127.0.0.1:18222)"
	@echo "  make test            - Run basic syntax check on Python files"
	@echo "  make clean           - Clean up temporary files"
	@echo ""
	@echo "Example usage:"
	@echo "  Terminal 1: make server"
	@echo "  Terminal 2: make client-test"

# Run server
server:
	@echo "Starting server on port $(SERVER_PORT)..."
	@echo "Press Ctrl+C to stop the server"
	$(PYTHON) $(SERVER)

# Run client (interactive - will prompt for IP/port)
client:
	@echo "Starting client..."
	@echo "Enter server IP and port when prompted, or use: make client-test"
	$(PYTHON) $(CLIENT)

# Run client with default server IP/port
client-test:
	@echo "Starting client connecting to $(SERVER_IP):$(SERVER_PORT)..."
	$(PYTHON) $(CLIENT) $(SERVER_IP) $(SERVER_PORT)

# Test: Check Python syntax
test:
	@echo "Checking Python syntax..."
	@$(PYTHON) -m py_compile $(CLIENT) && echo "✓ $(CLIENT) syntax OK" || echo "✗ $(CLIENT) has syntax errors"
	@$(PYTHON) -m py_compile $(SERVER) && echo "✓ $(SERVER) syntax OK" || echo "✗ $(SERVER) has syntax errors"
	@echo ""
	@echo "Syntax check complete. For full testing, run:"
	@echo "  Terminal 1: make server"
	@echo "  Terminal 2: make client-test"

# Clean (optional)
clean:
	@echo "Cleaning up..."
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "Clean complete."

# Phony targets
.PHONY: all help server client client-test test clean
