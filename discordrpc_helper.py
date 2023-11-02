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

        with open("dc_token.txt", "r", encoding="utf8") as file:
            token = file.readline()

        callbacks = {
            'ready': self._ready_callback,
            'disconnected': self._disconnected_callback,
            'error': self._error_callback,
        }

        discord_rpc.initialize(token, callbacks=callbacks, log=False)
        while not self.initialized:
            time.sleep(0.5)
            print("Waiting for discord rpc...", end="\r")
            self.show_rpc()

    def update(self, responded_count, not_responded_count, total_count):
        """Update stats shown in the discord rpc"""

        # if a new pass has started, last_sent gets reset
        if self.last_sent > (responded_count + not_responded_count):
            self.last_sent = 0
        # add the newly sent amount of pings to the total_pings
        self.total_pings += ((responded_count + not_responded_count) - self.last_sent)
        # update the newly sent amount of pings
        self.last_sent = (responded_count + not_responded_count)

        # if a new pass has started, alst_responded gets reset
        if self.last_responded > responded_count:
            self.last_responded = 0
        # add the newly sent amount of responded pings to the totla_responded
        self.total_responded += responded_count - self.last_responded
        # update the newly sent amount of pings
        self.last_responded = responded_count

        # update the shown stats
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
        """Update the connection of the discord rich presence"""

        discord_rpc.update_connection()
        time.sleep(2)
        discord_rpc.run_callbacks()

    def _ready_callback(self, current_user):
        """Callback when the discord rpc is ready"""

        if not self.initialized:
            print(f"Connected to user: {current_user['username']}#" +
                  f"{current_user['discriminator']}                                   ")
            self.initialized = True

    def _disconnected_callback(self, codeno, codemsg):
        """Callback when the discord rpc disconnects"""

        # do nothing

    def _error_callback(self, errno, errmsg):
        """Callback when the discord rpc errored"""

        # do nothing
