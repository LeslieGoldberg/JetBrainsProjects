import socket
import sys
import itertools
import string
import json
from datetime import datetime


class PasswordHack:
    def __init__(self, ip_address, port):
        """
        This class connects to a site and attempts to crack passwords.

        :param ip_address: The ip address of the service, from CLI
        :param port: The port of the service, from CLI
        """
        self.ip_address = ip_address
        self.port = int(port)

    def send_message(self, host_socket, message):
        message = message.encode('utf8')
        host_socket.send(message)
        return datetime.now()

    def receive_message(self, host_socket):
        response = host_socket.recv(1024)
        decoded_response = response.decode('utf8')
        return decoded_response

    def format_json_message(self, login, password):
        """
        Takes a login str and a password str and creates a JSON object.
        :param login: str from find_login
        :param password: empty while finding correct login, then str from find_password
        :return: JSON object
        """
        json_string = {
            "login": login,
            "password": password
        }
        return json.dumps(json_string)

    def common_logins(self):
        """
        Reads given txt file with most common logins and returns them one at a time.
        """
        with open('/Users/lesliegoldberg/PycharmProjects/Password Hacker/Password Hacker/task/hacking/logins.txt',
                  'r') as login_list:
            for login in login_list.readlines():
                yield login.rstrip('\n')

    def find_login(self, host_socket):
        """
        Finds login by attempting each login from txt file with most common logins sent in JSON format.
        Handles exceptions by returning the exception message.
        :return: login string
        """
        response = False

        for login in self.common_logins():
            self.send_message(host_socket, self.format_json_message(login, " "))
            message = self.receive_message(host_socket)
            received_message = json.loads(message)['result']

            if received_message == 'Wrong password!':
                response = login
                break
        return response

    def password_generator(self):
        """
        Generatively returns a single letter or number as a tuple.
        """
        while True:
            letters_and_numbers = itertools.chain(string.ascii_lowercase, string.ascii_uppercase, string.digits)
            yield from itertools.product(letters_and_numbers, repeat=1)

    def find_password(self, host_socket, login):
        """
        While loop finds one correct letter at a time until the password is correct.
        Uses time delay from server to determine when it is throwing an exception for the correct letter.

        :param host_socket: from PasswordHacker.__init__
        :param login: str from self.find_login()
        """
        response = False
        received_message = False
        password = []

        while received_message != 'Connection success!':
            for letter_tuple in self.password_generator():
                str_letter = "".join([x for x in letter_tuple])
                partial_password = "".join([x for x in password])
                guess_password = ''.join([partial_password, str_letter])
                sent_time = self.send_message(host_socket, self.format_json_message(login, guess_password))
                message = self.receive_message(host_socket)
                received_time = datetime.now()
                time_difference = (received_time - sent_time).total_seconds()
                received_message = json.loads(message)['result']

                if received_message == 'Connection success!':
                    response = guess_password
                    break
                elif time_difference >= 0.1:
                    password.append(str_letter)

        return response

    def run(self):
        with socket.socket() as host_socket:
            address = (self.ip_address, self.port)
            host_socket.connect(address)
            login = self.find_login(host_socket)
            if login:
                password = self.find_password(host_socket, login)
                response = self.format_json_message(login, password)
            else:
                response = 'No login'
            print(response)


if __name__ == '__main__':
    sys_args = sys.argv
    if len(sys_args) == 3:
        hack = PasswordHack(sys_args[1], sys_args[2])
        hack.run()
    else:
        print('Bad parameters')