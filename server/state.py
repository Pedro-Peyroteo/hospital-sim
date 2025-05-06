from multiprocessing import Manager

# Will manage shared memory: the triage queue and a thread-safe lock.
MAX_QUEUE_SIZE = 20
manager = Manager()
triage_queue = manager.Queue()
