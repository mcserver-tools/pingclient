"""Module containing the FindThread class"""

from socket import gaierror
from time import sleep

from mcstatus import JavaServer

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
            # exit of the server_finder ist exiting
            if self._server_finder.exited:
                self._server_finder._running_threads -= 1
                return

            # sleep while the server_finder is sleeping
            while self._server_finder.paused:
                sleep(0.1)
            self._ping_address(address)

        self._server_finder._running_threads -= 1

    def _ping_address(self, address):
        """Ping the given address"""

        try:
            JavaServer(address, 25565).ping(tries=1)

            # if the ping didn't cause an exception, the address works and gets saved
            self._server_finder.active_addresses[self._index_c][1].append(address)
            self._server_finder._responded_count += 1
        except gaierror as gaierr:
            raise gaierror(f"Address {address} can't be read!") from gaierr
        except IOError:
            # the most common outcome, if the ping timed out, the address didn't respond
            self._server_finder._not_responded_count += 1
        except IndexError as ierr:
            # some addresses cause an bytearray out of bounds exception, those get ignored
            if "bytearray index out of range" in ierr.args:
                self._server_finder._not_responded_count += 1
            else:
                raise ierr
