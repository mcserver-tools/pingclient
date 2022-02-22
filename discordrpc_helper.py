import time

import discord_rpc

class DiscordRpcHelper():
    def __init__(self):
        self.initialized = False
        self.start_time = time.time()
        self.total_pings = 0
        self.last_sent = 0

        token = open("pingclient/dc_token.txt", "r").readline()
        # Note: 'event_name': callback
        callbacks = {
            'ready': self.readyCallback,
            'disconnected': self.disconnectedCallback,
            'error': self.errorCallback,
        }

        discord_rpc.initialize(token, callbacks=callbacks, log=False)
        while not self.initialized:
            time.sleep(0.5)
            print("Waiting for discord rpc...", end="\r")
            self.show_rpc()

    def update(self, responded_count, not_responded_count, total_count, reset=False):
        self.total_pings += (responded_count + not_responded_count) - self.last_sent

        if not reset:
            self.last_sent = responded_count + not_responded_count
        else:
            self.last_sent = 0

        discord_rpc.update_presence(**{
            "details": f"Responded: {responded_count}, Total: {responded_count + not_responded_count}/{total_count}",
            "state": f"{self.total_pings} pings sent since starting",
            "start_timestamp": self.start_time,
            "large_image_key": "default"})
        self.show_rpc()

    def exit(self):
        discord_rpc.shutdown()

    def show_rpc(self):
        discord_rpc.update_connection()
        time.sleep(2)
        discord_rpc.run_callbacks()

    def readyCallback(self, current_user):
        # print('Connected to user: {}'.format(current_user))
        if not self.initialized:
            print(f"Connected to user: {current_user['username']}#{current_user['discriminator']}                                            ")
            self.initialized = True

    def disconnectedCallback(self, codeno, codemsg):
        # print('Disconnected from Discord rich presence. Code {}: {}                                        '.format(
        #     codeno, codemsg
        # ))
        pass

    def errorCallback(self, errno, errmsg):
        # print('An error occurred! Error {}: {}                                                  '.format(
        #     errno, errmsg
        # ))
        pass

if __name__ == "__main__":
    DiscordRpcHelper()
