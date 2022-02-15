from socket import create_connection

class Communicator():
    def __init__(self) -> None:
        self._address = ("192.168.0.154", 20005)

    def server_pingable(self, tries = 3):
        while tries > 0:
            try:
                sock = create_connection(self._address)
                self.send(sock, "PING")
                if self.recv(sock) == "200 OK":
                    return True
                tries -= 1
            except ConnectionRefusedError:
                tries -= 1
                print(f"Connection to server refused, retrying {tries} more times...", end="\r")
        return False

    def get_address(self):
        sock = create_connection(self._address)

        self.send(sock, "GET address")
        address = self.recv(sock)

        return address

    def send_addresses(self, client_address, addresses):
        sock = create_connection(self._address)

        self.send(sock, f"POST address {client_address} {str(addresses)}")
        answer = self.recv(sock)

        return answer == "200 OK"

    def send_keepalive(self, address):
        sock = create_connection(self._address)

        self.send(sock, f"KEEPALIVE {address}")
        answer = self.recv(sock)

        return answer == "200 OK"

    def send(self, sock, text):
        sock.send(self.StringToBytes(text))

    def recv(self, sock):
        return self.BytesToString(sock.recv(4096))

    @staticmethod
    def StringToBytes(input):
        return bytes(input, 'utf-8')

    @staticmethod
    def BytesToString(bytes):
        return bytes.decode()
