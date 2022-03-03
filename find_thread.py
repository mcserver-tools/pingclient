"""Module containing the FindThread class"""

from socket import gaierror

from mcstatus import MinecraftServer

# pylint: disable=R0903

class FindThread():
    """Class that pings all given addresses"""

    def __init__(self, addresses, server_finder, index_c) -> None:
        self._addresses = addresses
        self._server_finder = server_finder
        self._index_c = index_c

    def ping_all(self):
        """Ping all stored addresses"""

        for address in self._addresses:
            if self._server_finder.canceled:
                self._server_finder._running_threads -= 1
                return
            self._ping_address(address)

        self._server_finder._running_threads -= 1

    def _ping_address(self, address):
        """Ping the given address"""

        try:
            MinecraftServer(address, 25565).ping(1)

            self._server_finder.active_addresses[self._index_c][1].append(address)
            self._server_finder._responded_count += 1
        except gaierror as gaierr:
            raise gaierror(f"Address {address} can't be read!") from gaierr
        except IOError:
            self._server_finder._not_responded_count += 1
        except IndexError as ierr:
            if "bytearray index out of range" in ierr.args:
                self._server_finder._not_responded_count += 1
            else:
                raise ierr
