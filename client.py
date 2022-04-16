"""Module containing the Client class"""

from threading import Thread
from time import sleep

from gui import Gui
from server_finder import ServerFinder

class Client():
    """Class containing the main client functions"""

    def __init__(self) -> None:
        self._gui = None
        self._finder = None
        self._exit = False

        self._init_finder()

    def run(self):
        """Run the client"""

        # Thread(target=self.add_thread_func).start()
        Thread(target=self._run_finder).start()
        self._start_gui()

    def toggle_dcrpc(self):
        """Toggle the discord rpc once"""

        if self._finder.dcrpc_helper.initialized:
            self._finder.dcrpc_helper.exit()
        else:
            self._finder.dcrpc_helper.initialize()

    def exit(self):
        """Exit after the current pass"""

        self._exit = not self._exit

        while self._finder.running_threads > 0:
            if not self._exit:
                return False
            sleep(1)
        return True

    def cancel(self):
        """Exit immediately"""

        self._exit = True
        self._gui.show_console()
        self._finder.cancel()

        while self._finder.running_threads > 0:
            if not self._exit:
                return False
            sleep(1)
        return True

    def _start_gui(self):
        """Start the GUI"""

        self._gui = Gui(self.toggle_dcrpc, self._finder.pause, self.exit, self.cancel)
        self._gui.initialize()
        self._gui.run()

    def _run_finder(self):
        """Start pinging addresses"""

        try:
            while not self._exit:
                self._finder.run()
                sleep(1)
                while self._finder.running_threads > 0:
                    sleep(1)
                sleep(1)
        except Exception as e:
            self._exit = True
            sleep(1)
            Thread(target=self._gui.exit, daemon=True).start()
            sleep(1)
            raise e

    def _init_finder(self):
        """Initialize the client"""

        print("Starting client...\n")

        print("The following the performance modes exist:")
        print("(1) Low internet usage, 128 simultaneous threads")
        print("(2) Medium internet usage, 512 simultaneous threads (default)")
        print("(3) High internet usage, 2048 simultaneous threads (not recommended)")
        print("(4) Extreme internet usage, 8192 simultaneous threads ('just don't use it')")
        mode = input("Input the performance mode of your choice (default: 2): ")

        if mode == "1":
            finder_config = (128, 1)
        elif mode == "2":
            finder_config = (512, 3)
        elif mode == "3":
            finder_config = (2048, 3)
        elif mode == "4":
            finder_config = (8192, 9)
        else:
            print("Continuing with default...")
            finder_config = (512, 3)
        print("")

        print("Creating finder...")
        self._finder = ServerFinder(finder_config[0], finder_config[1], self._update_gui)
        print("Created finder object                                   \n")

    def _update_gui(self, session_info):
        """Add SessionInfo object to the GUI queue"""

        self._gui.queue.put(session_info)
