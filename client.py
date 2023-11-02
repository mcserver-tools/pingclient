"""Module containing the Client class"""

from threading import Thread
from time import sleep

# pylint: disable=E0401

import console_manager
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

        Thread(target=self._run_finder).start()
        self._start_gui()

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
        console_manager.show_console()
        self._finder.exit()

        while self._finder.running_threads > 0:
            if not self._exit:
                return False
            sleep(1)
        return True

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
            self._finder_config = (128, 1)
        elif mode == "2":
            self._finder_config = (512, 3)
        elif mode == "3":
            self._finder_config = (2048, 3)
        elif mode == "4":
            self._finder_config = (8192, 9)
        else:
            print("Continuing with default...")
            self._finder_config = (512, 3)
        print("")

    def _run_finder(self):
        """Start pinging addresses"""

        try:
            # loop until the client exits
            while not self._exit:
                self._finder = ServerFinder(self._finder_config[0], self._finder_config[1],
                                            self._update_gui)
                self._finder.run()
        # catch all exceptions, exit properly, and then rethrow the exception
        except Exception as exception:
            self._exit = True
            sleep(1)
            Thread(target=self._gui.exit, daemon=True).start()
            sleep(1)
            raise exception

    def _start_gui(self):
        """Start the GUI"""

        self._gui = Gui(self._toggle_dcrpc, self._pause, self.exit, self.cancel)
        self._gui.initialize()
        self._gui.run()

    def _pause(self):
        """Pause the client"""

        self._finder.pause()

    def _toggle_dcrpc(self):
        """Toggle the discord rpc once"""

        # if the discord rich resence is already active, deactivate it
        if self._finder.dcrpc_helper.initialized:
            self._finder.dcrpc_helper.exit()
        else:
            self._finder.dcrpc_helper.initialize()

    def _update_gui(self, session_info):
        """Add SessionInfo object to the GUI queue"""

        self._gui.queue.put(session_info)
