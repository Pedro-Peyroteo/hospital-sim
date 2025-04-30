from multiprocessing import Manager

# Will manage shared memory: the triage queue and a thread-safe lock.
manager = Manager()
triage_queue = manager.Queue()
