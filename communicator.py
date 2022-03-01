"""Module containing the Communicator class"""

from socket import create_connection

class Communicator():
    """Class for communication with the server"""

    def __init__(self) -> None:
        self._address = ("192.168.0.154", 20005)

    def server_pingable(self, tries = 3):
        """Return True if the server is pingable"""

        while tries > 0:
            try:
                sock = create_connection(self._address)
                self._send(sock, "PING")
                if self._recv(sock) == "200 OK":
                    return True
                tries -= 1
            except ConnectionRefusedError:
                tries -= 1
                print(f"Connection to server refused, retrying {tries} more times...", end="\r")
        return False

    def get_address(self):
        """Get new address range"""

        sock = create_connection(self._address)

        self._send(sock, "GET address")
        address = self._recv(sock)

        return address

    def send_addresses(self, client_address, addresses):
        """Send working addresses"""

        sock = create_connection(self._address)

        self._send(sock, f"POST address {client_address} {str(addresses)}")
        answer = self._recv(sock)

        return answer == "200 OK"

    def send_keepalive(self, address):
        """Send keepalive request"""

        sock = create_connection(self._address)

        self._send(sock, f"KEEPALIVE {address}")
        answer = self._recv(sock)

        return answer == "200 OK"

    def _send(self, sock, text):
        """Send string to thegiven socket"""

        sock.send(self._string_to_bytes(text))

    def _recv(self, sock):
        """Receive string from the given socket"""

        return self._bytes_to_string(sock.recv(4096))

    @staticmethod
    def _string_to_bytes(input_text):
        """Convert string to bytes object"""

        return bytes(input_text, 'utf-8')

    @staticmethod
    def _bytes_to_string(input_bytes):
        """Convert bytes object to string"""

        return input_bytes.decode()
