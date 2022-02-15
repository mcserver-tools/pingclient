from ctypes import WinDLL, windll
from pingclient.server_finder import ServerFinder

class GUI():
    def __init__(self) -> None:
        self.finder = None
        self._loop = False
        self._hide = False

        self.user32 = WinDLL('user32', use_last_error=True)

    def init(self):
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
            print("Couldn't read input, continuing with default...")
            finder_config = (2048, 3)
        print("")

        print("Creating finder...")
        self.finder = ServerFinder(finder_config[0], finder_config[1], self)
        print("Created finder object")

    def start(self):
        input_text = ""
        while input_text != "exit" and input_text != "quit" and input_text != "q":
            print("")
            input_text = input("> ")
            print("")
            if input_text.startswith("run"):
                if self._hide:
                    self._hide_console()
                if self._loop:
                    self.finder.run()
                    while self._loop:
                        self.finder.run()
                else:
                    if len(input_text.split(" ")) <= 1:
                        input_text += " 1"
                    try:
                        max_passes = int(input_text.split(" ")[1])
                    except:
                        print(f"Error: Couldn't convert count {input_text.split(' ')[1]}!")
                        max_passes = None
                    passes = 0
                    if max_passes != None:
                        while passes < max_passes:
                            passes += 1
                            self.finder.run()
                if self._hide:
                    self._show_console()
            elif input_text == "help":
                print(self._get_helptext())
            elif input_text == "loop":
                self._loop = not self._loop
                print(f"Toggled loop to {self._loop}")
            elif input_text == "hide":
                self._hide = not self._hide
                print(f"Toggled hide to {self._hide}")
            elif input_text == "exit" or input_text == "quit" or input_text == "q":
                print("Exiting...")
            else:
                print(f"Unknown command {input_text}")

    def _get_helptext(self):
        text = "Showing helptext:\n"
        text += "help   -->  Show this helptext\n"
        text += "run    -->  Start searching for addresses\n"
        text += "loop   -->  Toggle wether 'run' should loop infinitly\n"
        text += "hide   -->  Toggle wether this window hides after 'run'\n"
        text += "exit   -->  Exit client\n"
        text += "quit   -->  Exit client\n"
        text += "q      -->  Exit client"

        return text

    def _show_console(self):
        hWnd = windll.kernel32.GetConsoleWindow()
        SW_SHOW = 5
        WinDLL('user32', use_last_error=True).ShowWindow(hWnd, SW_SHOW)

    def _hide_console(self):
        hWnd = windll.kernel32.GetConsoleWindow()
        SW_HIDE = 0
        WinDLL('user32', use_last_error=True).ShowWindow(hWnd, SW_HIDE)
