# utils/logger.py
import time

class Logger:
    @staticmethod
    def log_event(event_type, peer_id, detail):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open("p2p_bazaar_log.txt", "a") as log_file:
            log_file.write(f"{timestamp} - Peer {peer_id}: {event_type} - {detail}\n")
