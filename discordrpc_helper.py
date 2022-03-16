"""Module containing the DiscordRpcHelper class"""

import time

import discord_rpc

class DiscordRpcHelper():
    """Class containing helping functions for the discord rich presence"""

    def __init__(self):
        self.initialized = False
        self.start_time = time.time()
        self.total_pings = 0
        self.last_sent = 0
        self.total_responded = 0
        self.last_responded = 0

    def initialize(self):
        """Initialize the discord rich presence"""

        with open("pingclient/dc_token.txt", "r", encoding="utf8") as file:
            token = file.readline()

        callbacks = {
            'ready': self.ready_callback,
            'disconnected': self.disconnected_callback,
            'error': self.error_callback,
        }

        discord_rpc.initialize(token, callbacks=callbacks, log=False)
        while not self.initialized:
            time.sleep(0.5)
            print("Waiting for discord rpc...", end="\r")
            self.show_rpc()

    def update(self, responded_count, not_responded_count, total_count):
        """Update stats shown in the discord rpc"""

        if self.last_sent > (responded_count + not_responded_count):
            self.last_sent = 0
        self.total_pings += ((responded_count + not_responded_count) - self.last_sent)
        self.last_sent = (responded_count + not_responded_count)

        if self.last_responded > responded_count:
            self.last_responded = 0
        self.total_responded += responded_count - self.last_responded
        self.last_responded = responded_count

        discord_rpc.update_presence(**{
            "details": f"Responded: {self.total_responded}, Total: " +
                       f"{responded_count + not_responded_count}/{total_count}",
            "state": f"{self.total_pings} pings sent since starting",
            "start_timestamp": self.start_time,
            "large_image_key": "default"})
        self.show_rpc()

    def exit(self):
        """Exit discord rich presence"""

        discord_rpc.shutdown()
        self.initialized = False

    @staticmethod
    def show_rpc():
        """Update discord rich presence"""

        discord_rpc.update_connection()
        time.sleep(2)
        discord_rpc.run_callbacks()

    def ready_callback(self, current_user):
        """Callback when the discord rpc is ready"""

        # print('Connected to user: {}'.format(current_user))
        if not self.initialized:
            print(f"Connected to user: {current_user['username']}#" +
                  f"{current_user['discriminator']}                                   ", end="\r")
            self.initialized = True

    def disconnected_callback(self, codeno, codemsg):
        """Callback when the discord rpc disconnects"""

        # print('Disconnected from Discord rich presence. Code {}: {}'.format(
        #     codeno, codemsg
        # ))

    def error_callback(self, errno, errmsg):
        """Callback when the discord rpc errored"""

        # print('An error occurred! Error {}: {}'.format(
        #     errno, errmsg
        # ))

if __name__ == "__main__":
    DiscordRpcHelper()
