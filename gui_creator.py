"""Module for creating the self.gui window"""

from threading import Thread
import tkinter

# pylint: disable=R0903, E0401

import console_manager

class GuiCreator:
    """Class for creating the Gui main window"""

    def __init__(self, gui) -> None:
        self.gui = gui

    def add_labels(self):
        """Adds labels to the main window"""

        # Main application header
        tkinter.Label(self.gui.main_frame, text="Ping Client", font=("", 30),
                      width=int(self.gui.SIZE[0] / 3), height=int(self.gui.SIZE[1] / 24)) \
               .pack(side=tkinter.TOP)

        # empty labels are whitespaces between the different sections
        self._add_global_labels()
        tkinter.Label(self.gui.main_frame).pack(side=tkinter.TOP)
        self._add_session_labels()
        tkinter.Label(self.gui.main_frame).pack(side=tkinter.TOP)
        self._add_working_addresses_labels()
        tkinter.Label(self.gui.main_frame).pack(side=tkinter.TOP)
        self._add_buttons()
        tkinter.Label(self.gui.main_frame).pack(side=tkinter.TOP)

    def _add_global_labels(self):
        """Add labels containing global information"""

        global_frame = tkinter.Frame(self.gui.main_frame, width=int(self.gui.SIZE[0]*6),
                                        height=int(self.gui.SIZE[1]),
                                        highlightbackground=self.gui.COLORS[0],
                                        highlightthickness=1)
        global_frame.pack_propagate(False)
        global_frame.pack(side=tkinter.TOP)

        # Global header
        tkinter.Label(global_frame, text="Global:", anchor="w").pack(fill="both")

        total_responded_frame = tkinter.Frame(global_frame, width=int(self.gui.SIZE[0]*6),
                                                height=int(self.gui.SIZE[1]/3))
        total_responded_frame.pack(side=tkinter.TOP)
        tkinter.Label(total_responded_frame, text="Responded:").pack(fill=tkinter.BOTH,
                                                                    side=tkinter.LEFT)
        tkinter.Label(total_responded_frame,
                      textvariable=self.gui.string_vars["total_responded_count"]) \
               .pack(fill=tkinter.BOTH, side=tkinter.RIGHT)

        total_active_frame = tkinter.Frame(global_frame, width=int(self.gui.SIZE[0]*6),
                                            height=int(self.gui.SIZE[1]/3))
        total_active_frame.pack(side=tkinter.TOP)
        tkinter.Label(total_active_frame, text="Total duration:").pack(fill=tkinter.BOTH,
                                                                    side=tkinter.LEFT)
        tkinter.Label(total_active_frame,
                      textvariable=self.gui.string_vars["total_active_time"]) \
               .pack(fill=tkinter.BOTH, side=tkinter.RIGHT)

    def _add_session_labels(self):
        """Add labels containing session information"""

        session_frame = tkinter.Frame(self.gui.main_frame, width=int(self.gui.SIZE[0]*6),
                                        height=int(self.gui.SIZE[1]*2),
                                        highlightbackground=self.gui.COLORS[0],
                                        highlightthickness=1)
        session_frame.pack_propagate(False)
        session_frame.pack(side=tkinter.TOP)

        # Session header
        tkinter.Label(session_frame, text="Session:", anchor="w").pack(fill="both")

        responded_frame = tkinter.Frame(session_frame, width=int(self.gui.SIZE[0]*6),
                                        height=int(self.gui.SIZE[1]/3))
        responded_frame.pack(side=tkinter.TOP)
        tkinter.Label(responded_frame, text="Responded:").pack(fill=tkinter.BOTH,
                                                               side=tkinter.LEFT)
        tkinter.Label(responded_frame, textvariable=self.gui.string_vars["responded_count"]) \
               .pack(fill=tkinter.BOTH, side=tkinter.RIGHT)

        addresses_frame = tkinter.Frame(session_frame, width=int(self.gui.SIZE[0]*6),
                                        height=int(self.gui.SIZE[1]/3))
        addresses_frame.pack(side=tkinter.TOP)
        tkinter.Label(addresses_frame, text="Total:").pack(fill=tkinter.BOTH, side=tkinter.LEFT)
        tkinter.Label(addresses_frame, textvariable=self.gui.string_vars["addresses_count"]) \
               .pack(fill=tkinter.BOTH, side=tkinter.RIGHT)

        addresses_percentage_frame = tkinter.Frame(session_frame, width=int(self.gui.SIZE[0]*6),
                                                    height=int(self.gui.SIZE[1]/3))
        addresses_percentage_frame.pack(side=tkinter.TOP)
        tkinter.Label(addresses_percentage_frame, text="Total percentage:").pack(fill=tkinter.BOTH,
                                                                                side=tkinter.LEFT)
        tkinter.Label(addresses_percentage_frame,
                      textvariable=self.gui.string_vars["addresses_percentage"]) \
               .pack(fill=tkinter.BOTH, side=tkinter.RIGHT)

        thread_frame = tkinter.Frame(session_frame, width=int(self.gui.SIZE[0]*6),
                                        height=int(self.gui.SIZE[1]/3))
        thread_frame.pack(side=tkinter.TOP)
        tkinter.Label(thread_frame, text="Active threads:").pack(side=tkinter.LEFT)
        tkinter.Label(thread_frame, textvariable=self.gui.string_vars["thread_counter"]) \
               .pack(side=tkinter.RIGHT)

        active_frame = tkinter.Frame(session_frame, width=int(self.gui.SIZE[0]*6),
                                        height=int(self.gui.SIZE[1]/3))
        active_frame.pack(side=tkinter.TOP)
        tkinter.Label(active_frame, text="Session duration:").pack(side=tkinter.LEFT)
        tkinter.Label(active_frame, textvariable=self.gui.string_vars["active_time"]) \
               .pack(side=tkinter.RIGHT)

    def _add_working_addresses_labels(self):
        """Add labels containing working addresses"""

        addresses_frame = tkinter.Frame(self.gui.main_frame, width=int(self.gui.SIZE[0]*6),
                                        height=int(self.gui.SIZE[1]*5.15),
                                        highlightbackground=self.gui.COLORS[0],
                                        highlightthickness=1)
        addresses_frame.pack_propagate(False)
        addresses_frame.pack(side=tkinter.TOP)

        # Working addresses header
        tkinter.Label(addresses_frame, text="Working addresses:", anchor="w").pack(fill="both")

        tkinter.Label(addresses_frame, textvariable=self.gui.string_vars["working_addresses"]) \
               .pack(side=tkinter.TOP)

    def _add_buttons(self):
        """Add buttons"""

        buttons_frame = tkinter.Frame(self.gui.main_frame, width=int(self.gui.SIZE[0]*6),
                                        height=int(self.gui.SIZE[1]),
                                        highlightbackground=self.gui.COLORS[0],
                                        highlightthickness=1)
        buttons_frame.pack_propagate(False)
        buttons_frame.pack(side=tkinter.TOP)

        other_buttons_frame = tkinter.Frame(buttons_frame, width=int(self.gui.SIZE[0]*6),
                                            height=int(self.gui.SIZE[1]/2))
        other_buttons_frame.pack_propagate(False)
        other_buttons_frame.pack(side=tkinter.TOP)

        tkinter.Checkbutton(other_buttons_frame, text="Discord rpc",
                            command=self.gui.callbacks["dcrpc"]).pack(side=tkinter.LEFT)
        tkinter.Button(other_buttons_frame, textvariable=self.gui.string_vars["pause_text"],
                       command=self._pause_and_change_text_func).pack(side=tkinter.RIGHT)

        exit_button_frame = tkinter.Frame(buttons_frame, width=int(self.gui.SIZE[0]*6),
                                          height=int(self.gui.SIZE[1]/2))
        exit_button_frame.pack_propagate(False)
        exit_button_frame.pack(side=tkinter.TOP)

        tkinter.Button(exit_button_frame, textvariable=self.gui.string_vars["exit_text"],
                       command=self._exit_after_passes_func).pack(side=tkinter.LEFT)
        tkinter.Button(exit_button_frame,
                       textvariable=self.gui.string_vars["exit_immediately_text"],
                       command=self._exit_immediately_func).pack(side=tkinter.RIGHT)

    def _pause_and_change_text_func(self):
        """Function getting called when pressing the pause button"""

        if self.gui.string_vars["pause_text"].get() == "Pause":
            self.gui.string_vars["pause_text"].set("Unpause")
        # if its already paused, unpause it
        else:
            self.gui.string_vars["pause_text"].set("Pause")

        # toggle the pause state
        self.gui.callbacks["pause"]()

    def _exit_after_passes_func(self):
        """Function getting called when pressing the 'Exit after current pass' button"""

        # if its already immediately exiting, do nothing
        if self.gui.string_vars["exit_immediately_text"].get() != "Exit immediately":
            return

        # start exiting after the current pass
        if self.gui.string_vars["exit_text"].get() == "Exit after current pass":
            console_manager.show_console()
            self.gui.string_vars["exit_text"].set("Exiting after current pass")
            Thread(target=self.gui.exit_after_current_pass).start()
        # stop exiting after the current pass
        else:
            console_manager.hide_console()
            self.gui.string_vars["exit_text"].set("Exit after current pass")

    def _exit_immediately_func(self):
        """Function getting called when pressing the 'Exit immediately button"""

        # if its already exiting after the current pass, do nothing
        if self.gui.string_vars["exit_text"].get() != "Exit after current pass":
            return

        # if its not already exiting, exit immediately
        if self.gui.string_vars["exit_immediately_text"].get() == "Exit immediately":
            console_manager.show_console()
            self.gui.string_vars["exit_immediately_text"].set("Exiting...")
            Thread(target=self.gui.exit).start()
