# TodoTracker

A client-server todo tracking application built with Python sockets. The server manages a shared todo list that multiple clients can connect to and interact with concurrently.

## Features

- **Multi-client support**: Server handles multiple concurrent connections using threading
- **Task management**: Add, list, remove, and mark tasks as completed/pending
- **Persistent session**: Tasks are maintained in server memory during the session
- **Simple protocol**: Line-based text protocol for easy debugging

## Requirements

- Python 3.x
- Linux/macOS/Windows (tested on Linux)

## Project Structure

```
CS3201/
├── TodoTrackerServer.py    # Server application
├── TodoTrackerClient.py    # Client application
├── Makefile                # Build and run commands
├── README.md              # This file
└── Report.pdf             # Project report
```

## Quick Start

### Using Makefile (Recommended)

1. **Start the server** (in one terminal):
   ```bash
   make server
   ```
   The server will start listening on port `18222`.

2. **Start a client** (in another terminal):
   ```bash
   make client-test
   ```
   This connects to `127.0.0.1:18222` by default.

   Or start interactively:
   ```bash
   make client
   ```
   You'll be prompted to enter the server IP and port.

### Manual Execution

1. **Start the server**:
   ```bash
   python3 TodoTrackerServer.py
   ```

2. **Start the client**:
   ```bash
   python3 TodoTrackerClient.py [IP] [PORT]
   ```
   
   Examples:
   ```bash
   # Connect to localhost on default port
   python3 TodoTrackerClient.py 127.0.0.1 18222
   
   # Interactive mode (will prompt for IP/port)
   python3 TodoTrackerClient.py
   ```

## Commands

The client supports the following commands:

### ADD
Add a new task to the todo list. Enter the task description line by line, and end with a line containing only `#`.

```
client: ADD
client: Buy groceries
client: Milk and eggs
client: #
server: OK
```

### LIST
Display all tasks in the todo list.

```
client: LIST
server: Happy Socket Programming
server: TASK ID: 0000 | RECEIVED TIME: 2025-01-15 10:00:00 | STATUS: pending
server: Buy groceries
server: Milk and eggs
server: #
```

### REMOVE
Remove one or more tasks by their IDs. Enter IDs line by line, and end with `#`.

```
client: REMOVE
client: 0000
client: 0001
client: #
server: OK
```

If any ID is invalid:
```
server: ERROR - Invalid ID
```

### MARK
Toggle the status of tasks (between `pending` and `completed`). Enter IDs line by line, and end with `#`.

```
client: MARK
client: 0000
client: #
server: OK
```

If any ID is invalid:
```
server: ERROR - Invalid ID
```

### QUIT
Disconnect from the server and exit the client.

```
client: QUIT
server: OK
```

## Protocol Details

- **Line-based communication**: All messages are terminated with `\n`
- **Multi-line input**: Commands that accept multiple lines (ADD, REMOVE, MARK) use `#` as the end marker
- **Error handling**: Invalid commands return `ERROR - Command not understood`
- **Connection**: Server listens on `0.0.0.0:18222` by default
- **Port validation**: Client validates that ports are between 1024 and 65535

## Architecture

### Server (`TodoTrackerServer.py`)
- Creates a TCP socket and listens on port 18222
- Uses threading to handle multiple concurrent clients
- Maintains a global task list in memory
- Each task has:
  - `id`: 4-digit zero-padded ID (e.g., "0000", "0001")
  - `time`: Timestamp when task was created
  - `status`: Either "pending" or "completed"
  - `content`: Multi-line task description

### Client (`TodoTrackerClient.py`)
- Connects to server via TCP socket
- Supports command-line arguments for IP/port or interactive input
- Implements command handlers for each operation
- Properly closes socket on QUIT

## Example Session

```
# Terminal 1: Server
$ make server
Server listening on port 18222...

# Terminal 2: Client
$ make client-test
Connected to 127.0.0.1:18222
Connected to server.
client: WRONG COMMAND
server: ERROR Command not understood
client: ADD
client: Buy groceries
client: Milk and eggs
client: #
server: OK
client: ADD
client: Attend CS3201
client: #
server: OK
client: LIST
server: Happy Socket Programming
STATUS: pending
server: TASK ID: 0000 | RECEIVED TIME: 2025-10-20 01:21:07 |
server: Buy groceries
server: Milk and eggs
server: TASK ID: 0001 | RECEIVED TIME: 2025-10-20 01:21:15 |
STATUS: pending
server: Attend CS3201
client: MARK
client: INVALID ID
client: #
server: ERROR Invalid ID
client: MARK
client:
0000
client: #
server: OK
client:
LIST
server: Happy Socket Programming
STATUS: completed
server: TASK ID: 0000 | RECEIVED TIME: 2025-10-20 01:21:07 |
server: Buy groceries
server: Milk and eggs
server: TASK ID: 0001 | RECEIVED TIME: 2025-10-20 01:21:15 |
STATUS: pending
server: Attend CS3201
client: REMOVE
client: INVALID ID
client: #
server: ERROR
Invalid ID
client: REMOVE
client: 0000
client:
0001
client: #
server: OK
client: LIST
server: Happy Socket Programming
client: QUIT
server: OK
```

## Makefile Commands

- `make server` - Start the server
- `make client` - Start client (interactive mode)
- `make client-test` - Start client with default settings (127.0.0.1:18222)
- `make test` - Check Python syntax
- `make clean` - Remove Python cache files
- `make help` - Show all available commands

## Notes

- Tasks are stored in server memory and will be lost when the server is restarted
- Task IDs are auto-generated and increment sequentially
- The server supports up to 20 concurrent connections
- All timestamps use the format: `YYYY-MM-DD HH:MM:SS`

## Troubleshooting

**Connection refused:**
- Ensure the server is running before starting the client
- Check that the IP address and port are correct
- Verify firewall settings allow the connection

**Port must be between 1024 and 65535:**
- The client validates port numbers. Use a port in the valid range.

**Invalid ID errors:**
- Task IDs are 4-digit zero-padded numbers (e.g., "0000", not "0")
- Ensure tasks exist before trying to REMOVE or MARK them

## License

This project is part of CS3201 coursework.

