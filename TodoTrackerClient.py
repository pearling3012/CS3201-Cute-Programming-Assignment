# TodoTrackerClient.py
import socket
import sys


def read_line():
    """
    Reads a single line of input from the user (used for commands or extra input).
    """
    return input("client: ").strip()


def read_multiline_input(sock):
    """
    Read user lines until '#'; send each line immediately to server.
    """
    while True:
        line = input("client: ")
        sock.sendall((line + "\n").encode("utf-8"))
        if line.strip() == "#":
            break


def send_line(sock, line):
    """
    Sends a single line (string) to the server with newline termination.
    """
    sock.sendall((line + "\n").encode("utf-8"))


def receive_line(sock):
    """
    Reads a single line (ending with '\n') from the server.
    Returns it as a decoded string (without newline).
    """
    data = b""
    while True:
        chunk = sock.recv(1)
        if not chunk:
            raise ConnectionError("Connection closed by server")
        data += chunk
        if chunk.endswith(b"\n"):
            break
    return data.decode("utf-8").strip()     

def receive_until_hash(sock):
    """
    Receives and prints multiple lines from the server until '#' is encountered.
    Used for LIST command responses that contain multiple lines.
    """
    while True:
        line = receive_line(sock)
        print("server:", line)
        if line.strip() == "#":
            break


# ---------------------------------
# TASK 1 — Initialize socket
# ---------------------------------
def initialize_socket():
    """Creates and returns a TCP socket."""
    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return client_sock
    except socket.error as e:
        print("Socket creation failed:", e)
        sys.exit(1)

# ---------------------------------
# TASK 2 — Connect to Server
# ---------------------------------

def connect_to_server(sock):
    """
    Get IP/port and connect with validation.
    """
    if len(sys.argv) == 3:
        ip = sys.argv[1].strip()
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("Error: Port must be an integer")
            sys.exit(1)
    else:
        ip = input("Enter server IP: ").strip()
        while True:
            try:
                port = int(input("Enter server Port: ").strip())
                break
            except ValueError:
                print("Error: Port must be an integer")

    # Validate port
    if not (1024 <= port <= 65535):
        print("Error: Port must be between 1024 and 65535")
        sys.exit(1)

    # Connect
    try:
        sock.connect((ip, port))
        print(f"Connected to {ip}:{port}")
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)


# ---------------------------------
# TASK 3, 4, 5 — Command handlers 
# ---------------------------------

def command_add(sock):
    """
    Handles the ADD command:
    1. Reads multi-line task description from the user until '#'.
    2. Sends each line to the server.
    3. Receives server response and prints it.
    """
    read_multiline_input(sock)
    response = receive_line(sock)
    print(f"server: {response}")

def command_list(sock):
    """
    Handles the LIST command:
    1. Receives multiple lines of task list from the server.
    2. Stops reading when '#' is encountered (end-of-list marker).
    3. Prints each line exactly as received (matching sample output).
    """
    while True:
        line = receive_line(sock)
        if line.strip() == "#":
            break
        print(f"server: {line}")

def command_remove(sock):
    read_multiline_input(sock)
    response = receive_line(sock)
    print(response)

def command_mark(sock):
    """
    Handles the MARK command:
    1. Reads task IDs to mark/unmark from the user until '#'.
    2. Sends each line to the server.
    3. Receives server response:
       - Prints "server: ERROR" + message if invalid IDs.
       - Prints "server: OK" if marking succeeded.
    """
    read_multiline_input(sock)
    response = receive_line(sock)
    print(f"server: {response}")

def command_quit(sock):
    """
    Handles the QUIT command:
    1. Receives server confirmation.
    2. Closes the socket and exits the program.
    """
    response = receive_line(sock)
    print(f"server: {response}")
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    sys.exit(0)

def command_wrong(sock):
    """
    Handles invalid/unknown commands:
    1. Receives error message from server.
    2. Prints it.
    """
    print(f"server: {receive_line(sock)}")


# -----------------------------
# Main
# -----------------------------
def main():
    sock = initialize_socket()
    connect_to_server(sock)
    print("Connected to server.")

    while True:
        command = read_line()
        if not command:
            continue
        
        send_line(sock, command)
        cmd = command.upper()

        if cmd == "ADD":
            command_add(sock)
        elif cmd == "LIST":
            command_list(sock)
        elif cmd == "REMOVE":
            command_remove(sock)
        elif cmd == "MARK":
            command_mark(sock)
        elif cmd == "QUIT":
            command_quit(sock)
        else:
            command_wrong(sock)


if __name__ == "__main__":
    main()
