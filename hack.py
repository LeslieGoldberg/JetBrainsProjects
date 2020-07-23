import socket
import sys

pass_list = sys.argv


class PasswordHack:
    def __init__(self, hack_list):
        self.ip_address = hack_list[1]
        self.port = int(hack_list[2])
        self.message = hack_list[3]

    def connect_to_host(self, client_socket):
        address = (self.ip_address, self.port)
        client_socket.connect(address)

    def send_message(self, client_socket):
        message = self.message.encode()
        client_socket.send(message)

    def receive_message(self, client_socket):
        response = client_socket.recv(1024)
        return response

    def print_message(self, response):
        response = response.decode()
        print(response)

    def main(self):
        with socket.socket() as client_socket:
            self.connect_to_host(client_socket)
            self.send_message(client_socket)
            self.print_message(self.receive_message(client_socket))


if __name__ == '__main__':
    if len(pass_list) == 4:
        hack = PasswordHack(pass_list)
        hack.main()
