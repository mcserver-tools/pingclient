"""Module containing the Gui class"""

import tkinter
from datetime import timedelta
from queue import Queue
from threading import Thread

# pylint: disable=E0401

import console_manager
from gui_creator import GuiCreator

# pylint: disable=R0902, R0914

class Gui():
    """Class containing GUI-related functions"""

    def __init__(self, dcrpc_func, pause_func, exit_func, cancel_func) -> None:
        """Initialize the Gui"""

        # create the root application
        self._root = tkinter.Tk(screenName=None, baseName=None, className="PingClient", useTk=True)
        self._root.resizable(False, False)
        self.main_frame = tkinter.Frame(self._root)
        self.main_frame.pack(side=tkinter.TOP)
        self.main_frame.tk_setPalette(background=self.COLORS[1], foreground=self.COLORS[0])

        self.string_vars = {}

        self._last_responded_count = 0
        self._last_total_count = 0
        self._last_global_time = None

        self.queue = Queue(maxsize=0)
        self.callbacks = {
            "dcrpc": dcrpc_func,
            "pause": pause_func,
            "exit": exit_func,
            "cancel": cancel_func
        }

    SIZE = (48, 64)
    COLORS = ("#C1C1C1", "#464545")

    def initialize(self):
        """Initialize the Gui"""

        self._create_stringvars()

        self._root.protocol("WM_DELETE_WINDOW", Thread(target=self.exit).start)

        GuiCreator(self).add_labels()

    def run(self):
        """Run the Gui"""

        self._read_queue()
        self._root.mainloop()

    def exit(self):
        """Exit the Gui"""

        self.callbacks["cancel"]()
        console_manager.show_console()
        self._root.quit()

    def exit_after_current_pass(self):
        """Exit the Gui after all threads have stopped"""

        self.callbacks["exit"]()
        console_manager.show_console()
        self._root.quit()

    def _create_stringvars(self):
        """Create stringvars and save them in the dictionary"""

        self.string_vars["working_addresses"] = tkinter.StringVar(value="")
        self.string_vars["responded_count"] = tkinter.StringVar(value="0/0")
        self.string_vars["addresses_count"] = tkinter.StringVar(value="0/0")
        self.string_vars["addresses_percentage"] = tkinter.StringVar(value="0%")
        self.string_vars["total_responded_count"] = tkinter.StringVar(value="0/0")
        self.string_vars["active_time"] = tkinter.StringVar(value="")
        self.string_vars["total_active_time"] = tkinter.StringVar(value="")
        self.string_vars["thread_counter"] = tkinter.StringVar(value="0/0")

        self.string_vars["pause_text"] = tkinter.StringVar(value="Pause")
        self.string_vars["exit_text"] = tkinter.StringVar(value="Exit after current pass")
        self.string_vars["exit_immediately_text"] = tkinter.StringVar(value="Exit immediately")

    def _read_queue(self):
        """Read new entries from the queue"""

        if not self.queue.empty():
            session_info = self.queue.get()
            self._update_stats(session_info)

        self._root.after(250, self._read_queue)

    def _update_stats(self, session_info):
        """Update showed stats from the GUI"""

        self._update_global_stats(session_info)
        self._update_session_stats(session_info)
        self._update_working_addresses(session_info)

    def _update_global_stats(self, session_info):
        """Update stats related to global information"""

        # reset if a new pass started
        if self._last_total_count > (session_info.responded_count +
                                     session_info.not_responded_count):
            self._last_total_count = (session_info.responded_count +
                                      session_info.not_responded_count)
        if self._last_responded_count > session_info.responded_count:
            self._last_responded_count = session_info.responded_count

        old_total_count_split = self.string_vars["total_responded_count"].get().split("/")
        # add the newly received total responded pings to the shown total responded pings
        responded = (int(old_total_count_split[0]) +
                    (session_info.responded_count - self._last_responded_count))
        # add the newly received total pings to the shown total pings
        total = (int(old_total_count_split[1]) +
                ((session_info.responded_count + session_info.not_responded_count) -
                self._last_total_count))

        self._last_responded_count = session_info.responded_count
        self._last_total_count = (session_info.responded_count + session_info.not_responded_count)

        self.string_vars["total_responded_count"].set(f"{responded}/{total}")

        self._update_total_active_time(session_info)

    def _update_total_active_time(self, session_info):
        """Update the total time label with the time passed since the last update"""

        old_time = self.string_vars["total_active_time"].get()
        # if old_time is empty, only use the new value
        if old_time == "":
            # split to remove milliseconds
            new_value = str(session_info.active_time).split(".", maxsplit=1)[0]
            self._last_global_time = session_info.active_time
            self.string_vars["total_active_time"].set(new_value)
            return

        # if a new pass has started, _last_global_time gets reset
        if self._last_global_time > session_info.active_time:
            self._last_global_time = session_info.active_time

        # if the program is running for longer than a day, save old number of days
        old_days = 0
        if ", " in old_time:
            # split days off of old time,
            # so "1 day, 3:14:42" will become "3:14:42"
            old_days, old_time = old_time.split(", ", maxsplit=1)
            # convert the days to a float
            old_days = float(old_days.split(" ", maxsplit=1)[0])

        # convert the old string to a timedelta object
        old_hours, old_minutes, old_seconds = old_time.split(":")
        old_timedelta = timedelta(days=old_days, hours=float(old_hours),
                                  minutes=float(old_minutes),
                                  seconds=float(old_seconds))
        # add the time passed since the last update
        new_timedelta = old_timedelta + (session_info.active_time - self._last_global_time)
        # split to remove milliseconds
        new_timedelta = str(new_timedelta).split(".", maxsplit=1)[0]
        self._last_global_time = session_info.active_time
        self.string_vars["total_active_time"].set(new_timedelta)

    def _update_session_stats(self, session_info):
        """Update stats related to session information"""

        responded_count = str(session_info.responded_count) + "/" + \
                          str(session_info.responded_count + session_info.not_responded_count)
        self.string_vars["responded_count"].set(responded_count)

        address_count = str(session_info.responded_count + session_info.not_responded_count) + \
                        "/" + str(session_info.total_addresses)
        self.string_vars["addresses_count"].set(address_count)

        address_percentage = str(int(((session_info.responded_count +
                                    session_info.not_responded_count) /
                                    session_info.total_addresses) * 100)) + "%"
        self.string_vars["addresses_percentage"].set(address_percentage)

        thread_counter = f"{session_info.active_threads}/{session_info.max_threads}"
        self.string_vars["thread_counter"].set(thread_counter)

        active_time = str(session_info.active_time).split('.', maxsplit=1)[0]
        self.string_vars["active_time"].set(active_time)

    def _update_working_addresses(self, session_info):
        """Update the working addresses display"""

        for address in session_info.working_addresses:
            saved_addresses = self.string_vars["working_addresses"].get()
            # ignore addresses already listed
            if not address in saved_addresses.split("\n"):
                if saved_addresses == "":
                    self.string_vars["working_addresses"].set(address)
                # if there are already 20 addresses shown, remove the oldest one
                elif len(saved_addresses.split("\n")) == 20:
                    self.string_vars["working_addresses"].set(saved_addresses
                                                              .split("\n", maxsplit=1)[1]
                                                              + "\n" + address)
                # if there are less than 20 addresses shown, add the new address to the end
                else:
                    self.string_vars["working_addresses"].set(saved_addresses + "\n" + address)
