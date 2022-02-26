from threading import Thread
from time import sleep

from pingclient.gui import Gui
from pingclient.server_finder import ServerFinder

class Client():
    def __init__(self) -> None:
        self._finder = None
        self._exit = False

        self._init_finder()

    def run(self):
        # Thread(target=self.add_thread_func).start()
        Thread(target=self._run_finder).start()
        self._start_gui()

    def exit(self):
        self._exit = not self._exit

        while self._finder._running_threads > 0:
            if not self._exit:
                return False
            sleep(1)
        return True

    def cancel(self):
        self._exit = not self._exit
        self._finder.cancel()

        while self._finder._running_threads > 0:
            if not self._exit:
                return False
            sleep(1)
        return True

    def _start_gui(self):
        self._gui = Gui(self.exit, self.cancel)
        self._gui.run()

    def _run_finder(self):
        while not self._exit:
            self._finder.run()
            sleep(1)
            while self._finder._running_threads > 0:
                sleep(1)
            sleep(1)

    def _init_finder(self):
        print("Starting client...")
        print("")

        print("The following the performance modes exist:")
        print("(1) Low performance, 256 simultaneous threads")
        print("(2) Medium performance, 2048 simultaneous threads (default)")
        print("(3) High performance, 8192 simultaneous threads (not recommended)")
        mode = input("Input the performance mode of your choice (default: 2): ")

        if mode == "1":
            finder_config = (256, 1)
        elif mode == "2":
            finder_config = (2048, 3)
        elif mode == "3":
            finder_config = (8192, 12)
        else:
            print("Continuing with default...")
            finder_config = (2048, 3)
        print("")

        print("Creating finder...")
        self._finder = ServerFinder(finder_config[0], finder_config[1], self._update_gui)
        print("Created finder object                                   ")
        print("")

    def _update_gui(self, session_info):
        self._gui.queue.put(session_info)
