from threading import Thread
from time import sleep

from pingclient.gui import Gui
from pingclient.server_finder import ServerFinder

class Client():
    def __init__(self) -> None:
        self._finder = None
        self._init_finder()

    def run(self):
        # Thread(target=self.add_thread_func).start()
        Thread(target=self._finder.run).start()
        self._start_gui()

    def _start_gui(self):
        self._gui = Gui()
        self._gui.run()

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

    def add_thread_func(self):
        for item in range(5):
            sleep(0.5)
            self.add_item_to_queue(item)

    def add_item_to_queue(self, item):
        self._gui.queue.put(f"Test|test|tst|{item}")
        self._gui.queue.put(self)
