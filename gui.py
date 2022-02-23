import tkinter
from queue import Queue
from ctypes import WinDLL, windll

class Gui():
    def __init__(self) -> None:
        self._size = (48, 64)
        self._colors = ("#C1C1C1", "#464545")

        self._root = tkinter.Tk(screenName=None, baseName=None, className="PingClient", useTk=True)
        self._root.resizable(False, False)
        self._main_frame = tkinter.Frame(self._root)
        self._main_frame.pack(side=tkinter.TOP)
        self._main_frame.tk_setPalette(background=self._colors[1], foreground=self._colors[0])

        self._working_addresses = tkinter.StringVar(value="1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20")
        self._responded_count = tkinter.StringVar(value="Responded: 0/0")
        self._addresses_count = tkinter.StringVar(value="Total: 0/0, 0%")
        self._total_responded_count = tkinter.StringVar(value="Responded: 0/0")
        self._active_time = tkinter.StringVar(value="Session duration: ")
        self._total_active_time = tkinter.StringVar(value="Total duration: ")
        self._thread_counter = tkinter.StringVar(value="Active threads: 0/0")

        self.queue = Queue(maxsize=0)

        self._add_labels()

    def run(self):
        self._read_queue()
        self._root.mainloop()

    def _add_labels(self):
        # title_label = tkinter.Label(self._main_frame, text="Ping Client", width=int(self._size[0]), height=int(self._size[1] / 8))
        title_label = tkinter.Label(self._main_frame, text="Ping Client", font=("", 30), width=int(self._size[0] / 3), height=int(self._size[1] / 24))
        title_label.pack(side=tkinter.TOP)

        self._add_global_labels()

        self._add_placeholder_label()

        self._add_session_labels()

        self._add_placeholder_label()

        self._add_working_addresses_labels()

        self._add_placeholder_label()

    def _add_global_labels(self):
        global_frame = tkinter.Frame(self._main_frame, width=int(self._size[0]*6), height=int(self._size[1]), highlightbackground=self._colors[0], highlightthickness=1)
        global_frame.pack_propagate(False)
        global_frame.pack(side=tkinter.TOP)

        global_label = tkinter.Label(global_frame, text="Global:", anchor="w")
        global_label.pack(fill="both")

        total_responded_count = tkinter.Label(global_frame, textvariable=self._total_responded_count)
        total_responded_count.pack(side=tkinter.TOP)

        total_active_time = tkinter.Label(global_frame, textvariable=self._total_active_time)
        total_active_time.pack(side=tkinter.TOP)

    def _add_session_labels(self):
        session_frame = tkinter.Frame(self._main_frame, width=int(self._size[0]*6), height=int(self._size[1]*2), highlightbackground=self._colors[0], highlightthickness=1)
        session_frame.pack_propagate(False)
        session_frame.pack(side=tkinter.TOP)
        
        session_label = tkinter.Label(session_frame, text="Session:", anchor="w")
        session_label.pack(fill="both")

        responded_count = tkinter.Label(session_frame, textvariable=self._responded_count)
        responded_count.pack(side=tkinter.TOP)

        addresses_count = tkinter.Label(session_frame, textvariable=self._addresses_count)
        addresses_count.pack(side=tkinter.TOP)

        thread_counter = tkinter.Label(session_frame, textvariable=self._thread_counter)
        thread_counter.pack(side=tkinter.TOP)

        active_time = tkinter.Label(session_frame, textvariable=self._active_time)
        active_time.pack(side=tkinter.TOP)

    def _add_working_addresses_labels(self):
        addresses_frame = tkinter.Frame(self._main_frame, width=int(self._size[0]*6), height=int(self._size[1]*5.15), highlightbackground=self._colors[0], highlightthickness=1)
        addresses_frame.pack_propagate(False)
        addresses_frame.pack(side=tkinter.TOP)

        addresses_label = tkinter.Label(addresses_frame, text="Working addresses:", anchor="w")
        addresses_label.pack(fill="both")

        working_addresses = tkinter.Label(addresses_frame, textvariable=self._working_addresses)
        working_addresses.pack(side=tkinter.TOP)

    def _add_placeholder_label(self):
        placeholder_label = tkinter.Label(self._main_frame)
        placeholder_label.pack(side=tkinter.TOP)

    def _read_queue(self):
        if not self.queue.empty():
            session_info = self.queue.get()
            self._update_stats(session_info)

        self._root.after(250, self._read_queue)

    def _update_stats(self, session_info):
        left = self._responded_count.get().split(': ')[0].strip()
        right = f"{session_info.responded_count}/{session_info.not_responded_count}"
        self._responded_count.set(self._pad(left, right))

        left = self._addresses_count.get().split(': ')[0].strip()
        right = f"{session_info.responded_count + session_info.not_responded_count}/{session_info.total_addresses}, {int(((session_info.responded_count + session_info.not_responded_count) / session_info.total_addresses) * 100)}%"
        self._addresses_count.set(self._pad(left, right))

        left = self._thread_counter.get().split(': ')[0].strip()
        right = f"{session_info.active_threads}/{session_info.max_threads}"
        self._thread_counter.set(self._pad(left, right))

        left = self._active_time.get().split(': ')[0].strip()
        right = f"{str(session_info.active_time).split('.')[0]}"
        self._active_time.set(self._pad(left, right))

    @staticmethod
    def _pad(left, right):
        if len(left) > len(right):
            diff = len(left) - len(right)
            right += " " * diff
        elif len(left) < len(right):
            diff = len(right) - len(left)
            left = (" " * diff) + left

        print(f"{len(left)}:{len(right)}")
        print(f"!{left}: {right}!")

        return f"{left}: {right}"

    @staticmethod
    def _pad2(left, right):
        if len(left) < 25:
            diff = 25 - len(left)
            left = (" " * diff) + left
        if len(right) < 25:
            diff = 25 - len(right)
            right += (" " * diff)

        # print(f"!{left}: {right}!")

        return f"{left}: {right}"

    def _show_console(self):
        hWnd = windll.kernel32.GetConsoleWindow()
        SW_SHOW = 5
        WinDLL('user32', use_last_error=True).ShowWindow(hWnd, SW_SHOW)

    def _hide_console(self):
        hWnd = windll.kernel32.GetConsoleWindow()
        SW_HIDE = 0
        WinDLL('user32', use_last_error=True).ShowWindow(hWnd, SW_HIDE)
