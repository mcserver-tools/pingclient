class SessionInfo():
    def __init__(self, working_addresses, total_addresses, responded_count, not_responded_count, active_time, max_threads, active_threads) -> None:
        self.working_addresses = working_addresses
        self.total_addresses = total_addresses
        self.responded_count = responded_count
        self.not_responded_count = not_responded_count
        self.active_time = active_time
        self.max_threads = max_threads
        self.active_threads = active_threads

    def __str__(self) -> str:
        text = "                                                                     \n"
        text += f"Responded: {self.responded_count}, No response: {self.not_responded_count}, Total: {self.responded_count + self.not_responded_count}/{self.total_addresses}\n"
        text += f"Max Threads: {self.max_threads}, Active threads: {self.active_threads}\n"
        text += f"Elapsed: {str(self.active_time).split('.')[0]}\n"
        text += "                                                                     "
        return text
