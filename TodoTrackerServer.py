# TodoTrackerServer.py

import socket
import threading
import datetime

# task list: [{'id': '0000', 'time': '2025-10-19 10:00:00', 'status': 'pending', 'content': 'Buy groceries\nMilk and eggs.'}]
tasks = []
next_id = 0

def generate_id():
    global next_id
    id_str = f"{next_id:04d}"
    next_id += 1
    return id_str

def read_line(conn):
    line = b''
    while True:
        chunk = conn.recv(1)
        if not chunk:
            raise ConnectionError("Connection closed unexpectedly")
        line += chunk
        if chunk.endswith(b'\n'):
            break
    return line.decode('utf-8').strip()

def read_until_hash(conn):
    lines = []
    while True:
        line = read_line(conn)
        if line == '#':
            break
        # if line:
        #     lines.append(line)
        lines.append(line)
    return lines

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    try:
        while True:
            # Read command line
            command_line = read_line(conn)
            if not command_line:
                continue
            command = command_line.upper()
            print(f"Command: {command}")

            if command == 'ADD':
                # Read multi-line content until #
                content_lines = read_until_hash(conn)
                content = '\n'.join(content_lines)

                # Add task
                task_id = generate_id()
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                tasks.append({
                    'id': task_id,
                    'time': timestamp,
                    'status': 'pending',
                    'content': content
                })
                print(f"Added task {task_id}: \n{content}")
                conn.send(b'OK\n')

            elif command == 'LIST':
                # Send all tasks
                response = ["Happy Socket Programming"]
                for task in tasks:
                    response.append(f"TASK ID: {task['id']} | RECEIVED TIME: {task['time']} | STATUS: {task['status']}")
                    for line in task['content'].split('\n'):
                        response.append(line)
                # response_str = '\n'.join(response) + '#\n'
                # conn.send(response_str.encode('utf-8'))
                response.append("#")
                for line in response:
                    line += "\n"
                    conn.send(line.encode('utf-8'))

            elif command == 'REMOVE':
                # Read IDs until #
                ids_to_remove = read_until_hash(conn)

                # First pass: Validate all IDs exist without modifying
                all_valid = True
                temp_tasks = tasks.copy()  # Snapshot for validation
                for tid in ids_to_remove:
                    if not tid.strip():
                        continue
                    found = False
                    for task in temp_tasks:
                        if task['id'] == tid:
                            found = True
                            break
                    if not found:
                        all_valid = False
                        break

                if all_valid:
                    # Second pass: Remove if all valid
                    for tid in ids_to_remove:
                        for i, task in enumerate(tasks):
                            if task['id'] == tid:
                                del tasks[i]
                                break
                    conn.send(b'OK\n')
                else:
                    conn.send(b'ERROR - Invalid ID\n')

            elif command == 'MARK':
                # Read IDs until #
                ids_to_mark = read_until_hash(conn)

                # First pass: Validate all IDs exist without modifying
                all_valid = True
                temp_tasks = tasks.copy()  # Snapshot for validation
                for tid in ids_to_mark:
                    if not tid.strip():
                        continue
                    found = False
                    for task in temp_tasks:
                        if task['id'] == tid:
                            found = True
                            break
                    if not found:
                        all_valid = False
                        break

                if all_valid:
                    # Second pass: Toggle status if all valid
                    for tid in ids_to_mark:
                        for task in tasks:
                            if task['id'] == tid:
                                task['status'] = 'completed' if task['status'] == 'pending' else 'pending'
                                break
                    conn.send(b'OK\n')
                else:
                    conn.send(b'ERROR - Invalid ID\n')

            elif command == 'QUIT':
                conn.send(b'OK\n')
                break

            else:
                conn.send(b'ERROR - Command not understood\n')

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        print(f"Connection closed from {addr}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 18222))
    server.listen(20)
    print("Server listening on port 18222...")

    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    main()