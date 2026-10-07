class ResponseManager:
    def __init__(self, audio_tools):
        self.audio = audio_tools
        self.last_spoken = {}
        import time
        self.time = time
        self.pending_messages = []

    def format_and_speak(self, message: str, priority: str = "NORMAL"):
        """
        Formats response and sends to Priority TTS, filtering out rapid repetitions.
        """
        # Deduplication based on exact message
        now = self.time.time()
        if message in self.last_spoken:
            if now - self.last_spoken[message] < 15.0: # 15 second cooldown for exact identical messages
                if priority not in ["CRITICAL", "HIGH"]: 
                    return
        self.last_spoken[message] = now
        self.pending_messages.append(message)
        self.audio.speak(message, priority)

    def get_pending_messages(self):
        msgs = self.pending_messages[:]
        self.pending_messages.clear()
        return msgs
