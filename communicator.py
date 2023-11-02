"""Module containing the Communicator class"""

import sys
from socket import create_connection

class Communicator():
    """Class for communicating with the server"""

    def __init__(self) -> None:
        if len(sys.argv) == 1:
            raise Exception("No address specified, exiting...")
        self._address = (sys.argv[1], 20005)

    def server_pingable(self, tries = 3):
        """Return True if the server is pingable"""

        while tries > 0:
            try:
                sock = create_connection(self._address, timeout=5.0)
                self._send(sock, "PING")
                if self._recv(sock) == "OK":
                    return True
                tries -= 1
            except (ConnectionRefusedError, TimeoutError):
                tries -= 1
                print(f"Connection to server failed, retrying {tries} more times...", end="\r")

        print("Connection to server failed                                ")
        return False

    def get_address(self):
        """Get new address range"""

        sock = create_connection(self._address)
        self._send(sock, "GET address")

        return self._recv(sock)

    def send_addresses(self, client_address, addresses):
        """Send working addresses"""

        sock = create_connection(self._address)
        self._send(sock, f"PUT address {client_address} {str(addresses)}")

        return self._recv(sock) == "OK"

    def send_keepalive(self, address):
        """Send keepalive request"""

        try:
            sock = create_connection(self._address)
            self._send(sock, f"KEEPALIVE {address}")
            answer = self._recv(sock)
        except (ConnectionRefusedError, TimeoutError):
            print("Sending keepalive to server failed, cancelling...")
            return False
        return answer == "OK"

    def _send(self, sock, text):
        """Send a string to the given socket"""

        sock.send(self._string_to_bytes(text))

    def _recv(self, sock):
        """Receive a string from the given socket"""

        return self._bytes_to_string(sock.recv(4096))

    @staticmethod
    def _string_to_bytes(input_text):
        """Convert a string to a bytes object"""

        return bytes(input_text, 'utf-8')

    @staticmethod
    def _bytes_to_string(input_bytes):
        """Convert a bytes object to a string"""

        return input_bytes.decode()
