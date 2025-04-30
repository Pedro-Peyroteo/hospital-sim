import socket
import threading
import time
import queue
import random

HOST = '0.0.0.0'
PORT = 5000
MAX_DOCTORS = 5


def handle_patient(conn, addr):
    print(f"[Hospital Server] New connection from {addr}")
        
    try: 
        data = conn.recv(1024).decode('utf-8')
        if data:
            print(f"[Hospital] Received from {addr}: {data}")
            conn.sendall("ACK from Hospital".encode('utf-8'))
    except Exception as e:
        print(f"[Hospital] Error with {addr}: {e}")
    finally:
        conn.close()
        print(f"[Hospital] Connection with {addr} closed.")


def hospital_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    
    print(f"[Hospital Server] Listening on {HOST}:{PORT}...")
    
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_patient, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    hospital_server()