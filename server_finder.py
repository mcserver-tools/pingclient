from datetime import datetime
from threading import Thread
from time import sleep

from pingclient.communicator import Communicator
from pingclient.find_thread import FindThread
from pingclient.discordrpc_helper import DiscordRpcHelper

class ServerFinder():
    def __init__(self, max_threads, max_passes, gui) -> None:
        self._max_threads = max_threads
        self._max_passes = max_passes

        self._total_addresses = 0
        self._running_threads = 0
        self._responded_count = 0
        self._not_responded_count = 0
        self.active_addresses = [["0.0.0.0", []]]
        self._cancel = False

        self._gui = gui
        self._dcrpc_helper = DiscordRpcHelper()

    def run(self):
        while not Communicator().server_pingable():
            timer = 60
            while timer > 0:
                print(f"Connecting to server failed, retrying in {timer} seconds...", end="\r")
                timer -= 1
                sleep(1)

        self._search()

    def _search(self):
        self._total_addresses = 0
        self._responded_count = 0
        self._not_responded_count = 0
        self.active_addresses.clear()
        self._cancel = False

        Thread(target=self._gui_func).start()
        Thread(target=self._keepalive_func).start()

        index_c = 0
        for addresses in self._get_addresses():
            if addresses == "Next":
                index_c += 1
            else:
                while self._running_threads >= self._max_threads:
                    sleep(0.05)

                find_thread = FindThread(addresses, self, index_c)
                Thread(target=find_thread.ping_all).start()
                self._running_threads += 1

        while self._running_threads > 0:
            sleep(1)

        sleep(1)
        for item in self.active_addresses:
            Communicator().send_addresses(item[0], item[1])

    def _get_addresses(self):
        passes = 0
        while not self._cancel and passes < self._max_passes:
            passes += 1

            self.active_addresses.append([Communicator().get_address(), []])
            first_number = self.active_addresses[-1][0].split(".")[0]
            second_number = self.active_addresses[-1][0].split(".")[1]
            print(f"Received address: {self.active_addresses[-1][0]}                                                          ")
            self._total_addresses += 256 * 256
            yield "Next"

            addresses = []
            for third_number in range(0, 256):
                for fourth_number in range(0, 256):
                    addresses.append(f"{first_number}.{second_number}.{third_number}.{fourth_number}")
                    if fourth_number % 32 == 0:
                        yield addresses.copy()
                        addresses.clear()
            yield addresses.copy()
            addresses.clear()

    def _keepalive_func(self):
        sleep(1)
        while self._running_threads > 0:
            for item in self.active_addresses:
                received = not Communicator().send_keepalive(item[0])
                if not self._cancel:
                    self._cancel = received
                if self._cancel:
                    break
            sleep(5)

    def _gui_func(self):
        start_time = datetime.now()
        c = 1
        sleep(1)
        while self._running_threads > 0:
            sleep(0.25)
            print("Responded: " + str(self._responded_count) + ", No response: " + str(self._not_responded_count) + ", Total: " + str(self._responded_count + self._not_responded_count) + "/" + str(self._total_addresses) + ", Elapsed: " + str(datetime.now() - start_time).split(".")[0], end="\r")
            if c >= 12:
                c = 0
                self._dcrpc_helper.update(self._responded_count, self._not_responded_count, self._total_addresses)
            c += 1

        self._dcrpc_helper.update(self._responded_count, self._not_responded_count, self._total_addresses, reset=True)
        print("Responded: " + str(self._responded_count) + ", No response: " + str(self._not_responded_count) + ", Total: " + str(self._responded_count + self._not_responded_count) + "/" + str(self._total_addresses) + ", Elapsed: " + str(datetime.now() - start_time).split(".")[0])