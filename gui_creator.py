import tkinter

def add_labels(gui):
    """Controls the addition of labels to the main window"""

    # Main application header
    tkinter.Label(gui._main_frame, text="Ping Client", font=("", 30), width=int(gui.SIZE[0] / 3), height=int(gui.SIZE[1] / 24)).pack(side=tkinter.TOP)

    _add_global_labels(gui)
    tkinter.Label(gui._main_frame).pack(side=tkinter.TOP)
    _add_session_labels(gui)
    tkinter.Label(gui._main_frame).pack(side=tkinter.TOP)
    _add_working_addresses_labels(gui)
    tkinter.Label(gui._main_frame).pack(side=tkinter.TOP)
    _add_buttons(gui)
    tkinter.Label(gui._main_frame).pack(side=tkinter.TOP)

    gui._hide_console()

def _add_global_labels(gui):
    """Add labels containing global information"""

    global_frame = tkinter.Frame(gui._main_frame, width=int(gui.SIZE[0]*6),
                                    height=int(gui.SIZE[1]),
                                    highlightbackground=gui.COLORS[0], highlightthickness=1)
    global_frame.pack_propagate(False)
    global_frame.pack(side=tkinter.TOP)

    # Global header
    tkinter.Label(global_frame, text="Global:", anchor="w").pack(fill="both")

    total_responded_frame = tkinter.Frame(global_frame, width=int(gui.SIZE[0]*6),
                                            height=int(gui.SIZE[1]/3))
    total_responded_frame.pack(side=tkinter.TOP)
    tkinter.Label(total_responded_frame, text="Responded:").pack(fill=tkinter.BOTH, side=tkinter.LEFT)
    tkinter.Label(total_responded_frame, textvariable=gui.string_vars["total_responded_count"]).pack(fill=tkinter.BOTH, side=tkinter.RIGHT)

    total_active_frame = tkinter.Frame(global_frame, width=int(gui.SIZE[0]*6),
                                        height=int(gui.SIZE[1]/3))
    total_active_frame.pack(side=tkinter.TOP)
    tkinter.Label(total_active_frame, text="Total duration:").pack(fill=tkinter.BOTH, side=tkinter.LEFT)
    tkinter.Label(total_active_frame, textvariable=gui.string_vars["total_active_time"]).pack(fill=tkinter.BOTH, side=tkinter.RIGHT)

def _add_session_labels(gui):
    """Add labels containing session information"""

    session_frame = tkinter.Frame(gui._main_frame, width=int(gui.SIZE[0]*6),
                                    height=int(gui.SIZE[1]*2),
                                    highlightbackground=gui.COLORS[0], highlightthickness=1)
    session_frame.pack_propagate(False)
    session_frame.pack(side=tkinter.TOP)

    # Session header
    tkinter.Label(session_frame, text="Session:", anchor="w").pack(fill="both")

    responded_frame = tkinter.Frame(session_frame, width=int(gui.SIZE[0]*6),
                                    height=int(gui.SIZE[1]/3))
    responded_frame.pack(side=tkinter.TOP)
    tkinter.Label(responded_frame, text="Responded:").pack(fill=tkinter.BOTH, side=tkinter.LEFT)
    tkinter.Label(responded_frame, textvariable=gui.string_vars["responded_count"]).pack(fill=tkinter.BOTH, side=tkinter.RIGHT)

    addresses_frame = tkinter.Frame(session_frame, width=int(gui.SIZE[0]*6),
                                    height=int(gui.SIZE[1]/3))
    addresses_frame.pack(side=tkinter.TOP)
    tkinter.Label(addresses_frame, text="Total:").pack(fill=tkinter.BOTH, side=tkinter.LEFT)
    tkinter.Label(addresses_frame, textvariable=gui.string_vars["addresses_count"]).pack(fill=tkinter.BOTH, side=tkinter.RIGHT)

    addresses_percentage_frame = tkinter.Frame(session_frame, width=int(gui.SIZE[0]*6),
                                                height=int(gui.SIZE[1]/3))
    addresses_percentage_frame.pack(side=tkinter.TOP)
    tkinter.Label(addresses_percentage_frame, text="Total percentage:").pack(fill=tkinter.BOTH, side=tkinter.LEFT)
    tkinter.Label(addresses_percentage_frame, textvariable=gui.string_vars["addresses_percentage"]).pack(fill=tkinter.BOTH, side=tkinter.RIGHT)

    thread_frame = tkinter.Frame(session_frame, width=int(gui.SIZE[0]*6),
                                    height=int(gui.SIZE[1]/3))
    thread_frame.pack(side=tkinter.TOP)
    tkinter.Label(thread_frame, text="Active threads:").pack(side=tkinter.LEFT)
    tkinter.Label(thread_frame, textvariable=gui.string_vars["thread_counter"]).pack(side=tkinter.RIGHT)

    active_frame = tkinter.Frame(session_frame, width=int(gui.SIZE[0]*6),
                                    height=int(gui.SIZE[1]/3))
    active_frame.pack(side=tkinter.TOP)
    tkinter.Label(active_frame, text="Session duration:").pack(side=tkinter.LEFT)
    tkinter.Label(active_frame, textvariable=gui.string_vars["active_time"]).pack(side=tkinter.RIGHT)

def _add_working_addresses_labels(gui):
    """Add labels containing working addresses"""

    addresses_frame = tkinter.Frame(gui._main_frame, width=int(gui.SIZE[0]*6),
                                    height=int(gui.SIZE[1]*5.15),
                                    highlightbackground=gui.COLORS[0], highlightthickness=1)
    addresses_frame.pack_propagate(False)
    addresses_frame.pack(side=tkinter.TOP)

    # Working addresses header
    tkinter.Label(addresses_frame, text="Working addresses:", anchor="w").pack(fill="both")

    tkinter.Label(addresses_frame, textvariable=gui.string_vars["working_addresses"]).pack(side=tkinter.TOP)

def _add_buttons(gui):
    """Add buttons"""

    other_buttons_frame = tkinter.Frame(gui._main_frame, width=int(gui.SIZE[0]*6),
                                    height=int(gui.SIZE[1]/2),
                                    highlightbackground=gui.COLORS[0],
                                    highlightthickness=1)
    other_buttons_frame.pack_propagate(False)
    other_buttons_frame.pack(side=tkinter.TOP)

    tkinter.Checkbutton(other_buttons_frame, text="Discord rpc", command=gui.callbacks["dcrpc"]).pack(side=tkinter.LEFT)

    tkinter.Button(other_buttons_frame, textvariable=gui.string_vars["pause_text"], command=gui._pause_and_change_text_func).pack(side=tkinter.RIGHT)

    exit_button_frame = tkinter.Frame(gui._main_frame, width=int(gui.SIZE[0]*6),
                                    height=int(gui.SIZE[1]/2),
                                    highlightbackground=gui.COLORS[0],
                                    highlightthickness=1)
    exit_button_frame.pack_propagate(False)
    exit_button_frame.pack(side=tkinter.TOP)

    tkinter.Button(exit_button_frame, textvariable=gui.string_vars["exit_text"], command=gui._exit_after_passes_func).pack(side=tkinter.LEFT)

    tkinter.Button(exit_button_frame, textvariable=gui.string_vars["exit_immediately_text"], command=gui._exit_immediately_func).pack(side=tkinter.RIGHT)

def _add_placeholder_label(gui):
    """Add a label as a placeholder"""

    tkinter.Label(gui._main_frame).pack(side=tkinter.TOP)
