"""Module ontaining the ServerFinder class"""

import time
from datetime import datetime
from threading import Thread
from time import sleep

from communicator import Communicator
from discordrpc_helper import DiscordRpcHelper
from find_thread import FindThread
from gui import Gui
from session_info import SessionInfo

# pylint: disable=R0902

class ServerFinder():
    """Class controlling all ping threads"""

    def __init__(self, max_threads, max_passes, gui_update_func) -> None:
        self._max_threads = max_threads
        self._max_passes = max_passes

        self._total_addresses = 0
        self._running_threads = 0
        self._responded_count = 0
        self._not_responded_count = 0
        self.active_addresses = []
        self._start_time = None
        self.canceled = False
        self.paused = False

        self._gui_update_func = gui_update_func
        self.dcrpc_helper = DiscordRpcHelper()

    def run(self):
        """Run one pass with the given configuration"""

        while not Communicator().server_pingable():
            timer = 60
            while timer > 0:
                print(f"Connecting to server failed, retrying in {timer} seconds...", end="\r")
                timer -= 1
                sleep(1)

        self._search()

    @property
    def running_threads(self):
        """Getter for _running_threads"""

        return self._running_threads

    def cancel(self):
        """Stop all ping threads and exit"""

        self.canceled = True
        Gui.show_console()

    def pause(self):
        """Pause or unpause all threads"""

        self.paused = not self.paused

    def _search(self):
        """Run one pass with the given configuration"""

        self._start_time = datetime.now()
        Gui.hide_console()

        # Thread(target=self._cli_func).start()
        Thread(target=self._gui_func).start()
        Thread(target=self._dcrpc_func).start()
        Thread(target=self._keepalive_func).start()

        index_c = -1
        for addresses in self._get_addresses():
            if addresses == "Next":
                index_c += 1
            elif addresses is None:
                break
            else:
                while self._running_threads >= self._max_threads:
                    sleep(0.05)

                find_thread = FindThread(addresses, self, index_c)
                Thread(target=find_thread.ping_all).start()
                self._running_threads += 1

        while self._running_threads > 0:
            sleep(1)

        if self.canceled:
            return

        sleep(1)
        for item in self.active_addresses:
            Communicator().send_addresses(item[0], item[1])

    def _get_addresses(self):
        """Yield addresses to give to client"""

        passes = 0
        while not self.canceled and passes < self._max_passes:
            passes += 1
            if not Communicator().server_pingable():
                self.cancel()
                return

            self.active_addresses.append([Communicator().get_address(), []])
            first_number = self.active_addresses[-1][0].split(".", maxsplit=1)[0]
            second_number = self.active_addresses[-1][0].split(".", maxsplit=2)[1]
            print(f"Received address: {self.active_addresses[-1][0]}" + \
                   "                                                          ")
            self._total_addresses += 256 * 256
            yield "Next"

            addr = []
            for third_number in range(0, 256):
                for fourth_number in range(0, 256):
                    addr.append(f"{first_number}.{second_number}.{third_number}.{fourth_number}")
                    if fourth_number % 32 == 0:
                        yield addr.copy()
                        addr.clear()
            yield addr.copy()
            addr.clear()

        yield None

    def _keepalive_func(self):
        """Send keepalive requests to the server"""

        sleep(1)
        while self._running_threads > 0:
            for item in self.active_addresses:
                if not Communicator().send_keepalive(item[0]):
                    self.cancel()
                    return
            sleep(5)

    def _gui_func(self):
        """Add SessionInfo objects to the GUI queue"""

        sleep(1)

        while self._running_threads > 0:
            start_time = time.time()
            working_addresses = []
            for item in self.active_addresses:
                working_addresses += item[1]
            session_info = SessionInfo(working_addresses,
                                       self._total_addresses, self._responded_count,
                                       self._not_responded_count,
                                       (datetime.now() - self._start_time), self._max_threads,
                                       self._running_threads)
            self._gui_update_func(session_info)
            sleep(1.0 - (time.time() - start_time))

        working_addresses = []
        for item in self.active_addresses:
            working_addresses += item[1]
        session_info = SessionInfo(working_addresses,
                                   self._total_addresses, self._responded_count,
                                   self._not_responded_count, (datetime.now() - self._start_time),
                                   self._max_threads, self._running_threads)
        self._gui_update_func(session_info)

    def _cli_func(self):
        """Print out different stats"""

        sleep(1)
        while self._running_threads > 0:
            start_time = time.time()
            print("Responded: " + str(self._responded_count) + ", No response: " +
                  str(self._not_responded_count) + ", Total: " + str(self._responded_count +
                  self._not_responded_count) + "/" + str(self._total_addresses) + ", Elapsed: " +
                  str(datetime.now() - self._start_time).split(".", maxsplit=1)[0], end="\r")
            sleep(0.5 - (time.time() - start_time))

        print("Responded: " + str(self._responded_count) + ", No response: " +
              str(self._not_responded_count) + ", Total: " + str(self._responded_count +
              self._not_responded_count) + "/" + str(self._total_addresses) + ", Elapsed: " +
              str(datetime.now() - self._start_time).split(".",maxsplit=1)[0])

    def _dcrpc_func(self):
        """Update the discord rich presence"""

        sleep(1)
        while self._running_threads > 0:
            start_time = time.time()
            self.dcrpc_helper.update(self._responded_count, self._not_responded_count,
                                      self._total_addresses)
            sleep(3.0 - (time.time() - start_time))

        self.dcrpc_helper.update(self._responded_count, self._not_responded_count,
                                  self._total_addresses)
