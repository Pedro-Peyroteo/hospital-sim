import socket
import threading
import time

messages = []

def listen_to_hospital_broadcast(host='hospital', port=5999):
    def listen():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Retry connection
            for _ in range(10):
                try:
                    s.connect((host, port))
                    print("[Dashboard] Connected to hospital server")
                    break
                except ConnectionRefusedError:
                    print("[Dashboard] Hospital not ready, retrying in 1s...")
                    time.sleep(1)
            else:
                print("[Dashboard] Failed to connect to hospital after retries.")
                return

            # Listen for data
            while True:
                data = s.recv(1024).decode('utf-8')
                if data:
                    print("[Dashboard] Received:", data.strip())
                    messages.append(data.strip())
                    if len(messages) > 100:
                        messages.pop(0)

        except Exception as e:
            print(f"[Dashboard] Error: {e}")

    thread = threading.Thread(target=listen, daemon=True)
    thread.start()
