import socket
import threading
import time
import json

messages = []
threads_info = {}

def listen_to_hospital_broadcast(host='hospital', port=5999):
    def listen():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

            buffer = ""
            while True:
                data = s.recv(1024).decode('utf-8')
                buffer += data

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line:
                        try:
                            msg = json.loads(line.strip())
                            msg.setdefault("timestamp", time.time())
                            msg_type = msg.get("type")

                            if msg_type == "thread_info":
                                print("[Dashboard] Thread info received:", msg)
                                threads_info.update(msg)
                            else:
                                if "type" in msg and "payload" in msg:
                                    print(f"[Dashboard] Event stored: {msg['type']}")
                                    messages.append(msg)

                                if len(messages) > 100:
                                    messages.pop(0)

                        except json.JSONDecodeError:
                            print("[Dashboard] Failed to parse:", line.strip())

        except Exception as e:
            print(f"[Dashboard] Error: {e}")

    thread = threading.Thread(target=listen, daemon=True)
    thread.start()
