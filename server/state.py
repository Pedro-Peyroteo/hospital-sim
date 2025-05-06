from multiprocessing import Manager

# Will manage shared memory: the triage queue and a thread-safe lock.
MAX_QUEUE_SIZE = 20
MAX_WAIT_TIME = 15

manager = Manager()

# Thread-safe shared resources.
triage_queue = manager.Queue()
waiting_patients = manager.dict()  # patient_id -> timestamp.