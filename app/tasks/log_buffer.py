import logging
from threading import Lock

log_buffer = []
log_buffer_lock = Lock()

def add_log_to_buffer(log_data):

    print("HERE -- 3")
    with log_buffer_lock:
        print("HERE -- 4")
        log_buffer.append(log_data)
        print("logbuffer: ", log_buffer)
        logging.info(f"LOG BUFFER -- {log_buffer}")
