import socket
import json
from sys import argv, exit

HOST = "127.0.0.1"  # Standard loopback interface address
PORT = 9090
server_login = "AdMinIstraTor"
server_password = "7yPrZq6"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    try:
        sock.listen()
        conn, addr = sock.accept()  # blocks execution, waits for incoming connection
        print("Connection Established!")
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                data = data.decode()
                data = json.loads(data)
                if data.get("login") == server_login:
                    if data.get("password") == server_password:
                        conn.sendall(json.dumps({"result": "Success!"}).encode('utf-8'))
                    elif server_password.startswith(data.get("password")):
                        conn.sendall(json.dumps({"result": "Exception happened during login!"}).encode('utf-8'))
                    else:
                        conn.sendall(json.dumps({"result": "Wrong password!"}).encode('utf-8'))
                else:
                    conn.sendall(json.dumps({"result": "Wrong login!"}).encode('utf-8'))
    except Exception as e:
        print(f"An error->{e} occurred!")
        exit()
