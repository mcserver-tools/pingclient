"""Module containing the Gui class"""

import tkinter
from ctypes import WinDLL, windll
from datetime import datetime, timedelta
from queue import Queue
from threading import Thread

# pylint: disable=R0902, R0914

class Gui():
    """Class containing GUI-related functions"""

    def __init__(self, exit_func, cancel_func) -> None:
        """Initialize the Gui"""

        self._size = (48, 64)
        self._colors = ("#C1C1C1", "#464545")

        self._root = tkinter.Tk(screenName=None, baseName=None, className="PingClient", useTk=True)
        self._root.resizable(False, False)
        self._main_frame = tkinter.Frame(self._root)
        self._main_frame.pack(side=tkinter.TOP)
        self._main_frame.tk_setPalette(background=self._colors[1], foreground=self._colors[0])

        self._working_addresses = tkinter.StringVar(value="1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n" + \
                                                          "12\n13\n14\n15\n16\n17\n18\n19\n20")
        self._responded_count = tkinter.StringVar(value="0/0")
        self._addresses_count = tkinter.StringVar(value="0/0")
        self._addresses_percentage = tkinter.StringVar(value="0%")
        self._total_responded_count = tkinter.StringVar(value="0/0")
        self._active_time = tkinter.StringVar(value="")
        self._total_active_time = tkinter.StringVar(value="")
        self._thread_counter = tkinter.StringVar(value="0/0")

        self._exit_text = tkinter.StringVar(value="Exit after current pass")
        self._exit_immediately_text = tkinter.StringVar(value="Exit immediately")

        self._last_responded_count = 0
        self._last_total_count = 0
        self._last_active_time = None

        self.queue = Queue(maxsize=0)
        self._exit_func = exit_func
        self._cancel_func = cancel_func

    def run(self):
        """Run the Gui"""

        self._read_queue()
        self._root.mainloop()

    def add_labels(self):
        """Controls the addition of labels to the main window"""

        title_label = tkinter.Label(self._main_frame, text="Ping Client", font=("", 30),
                                    width=int(self._size[0] / 3), height=int(self._size[1] / 24))
        title_label.pack(side=tkinter.TOP)

        self._add_global_labels()

        self._add_placeholder_label()

        self._add_session_labels()

        self._add_placeholder_label()

        self._add_working_addresses_labels()

        self._add_placeholder_label()

        self._add_buttons()

        self._add_placeholder_label()

    def _add_global_labels(self):
        """Add labels containing global information"""

        global_frame = tkinter.Frame(self._main_frame, width=int(self._size[0]*6),
                                     height=int(self._size[1]),
                                     highlightbackground=self._colors[0], highlightthickness=1)
        global_frame.pack_propagate(False)
        global_frame.pack(side=tkinter.TOP)

        global_label = tkinter.Label(global_frame, text="Global:", anchor="w")
        global_label.pack(fill="both")

        total_responded_frame = tkinter.Frame(global_frame, width=int(self._size[0]*6),
                                              height=int(self._size[1]/3))
        total_responded_frame.pack_propagate(False)
        total_responded_frame.pack(side=tkinter.TOP)
        total_responded_label = tkinter.Label(total_responded_frame, text="Responded: ", anchor="e")
        total_responded_label.pack(fill=tkinter.BOTH, side=tkinter.LEFT)
        total_responded_count = tkinter.Label(total_responded_frame,
                                              textvariable=self._total_responded_count)
        total_responded_count.pack(fill=tkinter.BOTH, side=tkinter.RIGHT)

        total_active_frame = tkinter.Frame(global_frame, width=int(self._size[0]*6),
                                           height=int(self._size[1]/3))
        total_active_frame.pack_propagate(False)
        total_active_frame.pack(side=tkinter.TOP)
        total_active_label = tkinter.Label(total_active_frame, text="Total duration: ", anchor="e")
        total_active_label.pack(fill=tkinter.BOTH, side=tkinter.LEFT)
        total_active_time = tkinter.Label(total_active_frame, textvariable=self._total_active_time)
        total_active_time.pack(fill=tkinter.BOTH, side=tkinter.RIGHT)

    def _add_session_labels(self):
        """Add labels containing session information"""

        session_frame = tkinter.Frame(self._main_frame, width=int(self._size[0]*6),
                                      height=int(self._size[1]*2),
                                      highlightbackground=self._colors[0], highlightthickness=1)
        session_frame.pack_propagate(False)
        session_frame.pack(side=tkinter.TOP)

        session_label = tkinter.Label(session_frame, text="Session:", anchor="w")
        session_label.pack(fill="both")

        responded_frame = tkinter.Frame(session_frame, width=int(self._size[0]*6),
                                        height=int(self._size[1]/3))
        responded_frame.pack_propagate(False)
        responded_frame.pack(side=tkinter.TOP)
        responded_label = tkinter.Label(responded_frame, text="Responded: ", anchor="e")
        responded_label.pack(fill=tkinter.BOTH, side=tkinter.LEFT)
        responded_count = tkinter.Label(responded_frame, textvariable=self._responded_count,
                                        anchor="w")
        responded_count.pack(fill=tkinter.BOTH, side=tkinter.RIGHT)

        addresses_frame = tkinter.Frame(session_frame, width=int(self._size[0]*6),
                                        height=int(self._size[1]/3))
        addresses_frame.pack_propagate(False)
        addresses_frame.pack(side=tkinter.TOP)
        addresses_label = tkinter.Label(addresses_frame, text="Total: ", anchor="e")
        addresses_label.pack(fill=tkinter.BOTH, side=tkinter.LEFT)
        addresses_count = tkinter.Label(addresses_frame, textvariable=self._addresses_count,
                                        anchor="w")
        addresses_count.pack(fill=tkinter.BOTH, side=tkinter.RIGHT)

        addresses_percentage_frame = tkinter.Frame(session_frame, width=int(self._size[0]*6),
                                                   height=int(self._size[1]/3))
        addresses_percentage_frame.pack_propagate(False)
        addresses_percentage_frame.pack(side=tkinter.TOP)
        addresses_percentage_label = tkinter.Label(addresses_percentage_frame,
                                                   text="Total percentage: ", anchor="e")
        addresses_percentage_label.pack(fill=tkinter.BOTH, side=tkinter.LEFT)
        addresses_percentage = tkinter.Label(addresses_percentage_frame,
                                             textvariable=self._addresses_percentage, anchor="w")
        addresses_percentage.pack(fill=tkinter.BOTH, side=tkinter.RIGHT)

        thread_frame = tkinter.Frame(session_frame, width=int(self._size[0]*6),
                                     height=int(self._size[1]/3))
        thread_frame.pack_propagate(False)
        thread_frame.pack(side=tkinter.TOP)
        thread_label = tkinter.Label(thread_frame, text="Active threads: ", anchor="e")
        thread_label.pack(side=tkinter.LEFT)
        thread_counter = tkinter.Label(thread_frame, textvariable=self._thread_counter, anchor="w")
        thread_counter.pack(side=tkinter.RIGHT)

        active_frame = tkinter.Frame(session_frame, width=int(self._size[0]*6),
                                     height=int(self._size[1]/3))
        active_frame.pack_propagate(False)
        active_frame.pack(side=tkinter.TOP)
        active_label = tkinter.Label(active_frame, text="Session duration: ", anchor="e")
        active_label.pack(side=tkinter.LEFT)
        active_time = tkinter.Label(active_frame, textvariable=self._active_time, anchor="w")
        active_time.pack(side=tkinter.RIGHT)

    def _add_working_addresses_labels(self):
        """Add labels containing working addresses"""

        addresses_frame = tkinter.Frame(self._main_frame, width=int(self._size[0]*6),
                                        height=int(self._size[1]*5.15),
                                        highlightbackground=self._colors[0], highlightthickness=1)
        addresses_frame.pack_propagate(False)
        addresses_frame.pack(side=tkinter.TOP)

        addresses_label = tkinter.Label(addresses_frame, text="Working addresses:", anchor="w")
        addresses_label.pack(fill="both")

        working_addresses = tkinter.Label(addresses_frame, textvariable=self._working_addresses)
        working_addresses.pack(side=tkinter.TOP)

    def _add_buttons(self):
        """Add buttons to exit"""

        button_frame = tkinter.Frame(self._main_frame, width=int(self._size[0]*6),
                                     height=int(self._size[1]/2),
                                     highlightbackground=self._colors[0],
                                     highlightthickness=1)
        button_frame.pack_propagate(False)
        button_frame.pack(side=tkinter.TOP)

        exit_button = tkinter.Button(button_frame, textvariable=self._exit_text,
                                     command=self._exit_after_passes_func, anchor="e")
        exit_button.pack(side=tkinter.LEFT)

        exit_immediately_button = tkinter.Button(button_frame,
                                                 textvariable=self._exit_immediately_text,
                                                 command=self._exit_immediately_func, anchor="w")
        exit_immediately_button.pack(side=tkinter.RIGHT)

    def _add_placeholder_label(self):
        """Add a label as a placeholder"""

        placeholder_label = tkinter.Label(self._main_frame)
        placeholder_label.pack(side=tkinter.TOP)

    def _exit_after_passes_func(self):
        """Function getting called when pressing the 'Exit after current pass' button"""

        if self._exit_immediately_text.get() != "Exit immediately":
            return
        if self._exit_text.get() == "Exit after current pass":
            self._exit_text.set("Exiting after current pass")
            Thread(target=self._exit_thread_func, args=[self._exit_func]).start()
        else:
            self._exit_text.set("Exit after current pass")

    def _exit_immediately_func(self):
        """Function getting called when pressing the 'Exit immediately button"""

        if self._exit_text.get() != "Exit after current pass":
            return
        if self._exit_immediately_text.get() == "Exit immediately":
            self._exit_immediately_text.set("Exiting...")
            Thread(target=self._exit_thread_func, args=[self._cancel_func]).start()

    def _exit_thread_func(self, func):
        """Function waiting for all threads to stop, then exit the GUI"""

        if func():
            self._root.quit()

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

    def _update_global_stats(self, session_info):
        """Update stats related to global information"""

        if self._last_total_count > (session_info.responded_count +
                                     session_info.not_responded_count):
            self._last_total_count = (session_info.responded_count +
                                      session_info.not_responded_count)
        if self._last_responded_count > session_info.responded_count:
            self._last_responded_count = session_info.responded_count
        responded = (int(self._total_responded_count.get().split("/")[0]) + \
                     (session_info.responded_count - self._last_responded_count))
        total = (int(self._total_responded_count.get().split("/")[1]) +
                 (session_info.responded_count + session_info.not_responded_count) -
                 self._last_total_count)
        right = f"{responded}/{total}"
        self._last_responded_count = session_info.responded_count
        self._last_total_count = (session_info.responded_count + session_info.not_responded_count)
        self._total_responded_count.set(right)

        if self._total_active_time.get() == "":
            right = str(session_info.active_time).split('.', maxsplit=1)[0]
        else:
            old_total_datetime = datetime.strptime(self._total_active_time.get(), '%H:%M:%S')
            if self._last_active_time > session_info.active_time:
                self._last_active_time = session_info.active_time
            new_timedelta = session_info.active_time - self._last_active_time
            right = str(timedelta(hours=old_total_datetime.hour, minutes=old_total_datetime.minute,
                                  seconds=old_total_datetime.second) + new_timedelta) \
                                  .split('.', maxsplit=1)[0]
        self._last_active_time = session_info.active_time
        self._total_active_time.set(right)

    def _update_session_stats(self, session_info):
        """Update stats related to session information"""

        right = str(session_info.responded_count) + "/" + \
                str(session_info.responded_count + session_info.not_responded_count)
        self._responded_count.set(right)

        right = str(session_info.responded_count + session_info.not_responded_count) + "/" + \
                str(session_info.total_addresses)
        self._addresses_count.set(right)

        right = str(int(((session_info.responded_count + session_info.not_responded_count) /
                session_info.total_addresses) * 100)) + "%"
        self._addresses_percentage.set(right)

        right = f"{session_info.active_threads}/{session_info.max_threads}"
        self._thread_counter.set(right)

        right = str(session_info.active_time).split('.', maxsplit=1)[0]
        self._active_time.set(right)

    @staticmethod
    def _show_console():
        """Show the console window"""

        window_handle = windll.kernel32.GetConsoleWindow()
        # SW_SHOW = 5
        show_flag = 5
        WinDLL('user32', use_last_error=True).ShowWindow(window_handle, show_flag)

    @staticmethod
    def _hide_console():
        """Hide the console window"""

        window_handle = windll.kernel32.GetConsoleWindow()
        # SW_HIDE = 0
        hide_flag = 0
        WinDLL('user32', use_last_error=True).ShowWindow(window_handle, hide_flag)
