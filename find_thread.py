from database import db_manager
from mcstatus import MinecraftServer

class FindThread():
    def __init__(self, addresses, server_finder, index_c) -> None:
        self._addresses = addresses
        self._server_finder = server_finder
        self._index_c = index_c

    def ping_all(self):
        for address in self._addresses:
            if self._server_finder._cancel:
                return
            self._ping_address(address)

        self._server_finder._running_threads -= 1

    def _ping_address(self, address):
        try:
            MinecraftServer(address, 25565).ping(1)

            self._server_finder.active_addresses[self._index_c][1].append(address)
            self._server_finder._responded_count += 1
        except:
            self._server_finder._not_responded_count += 1
