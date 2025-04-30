import socket
import threading

connected_dashboards = []

def start_dashboard_listener(host='0.0.0.0', port=5999):
    def listener():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            
            print(f"[Dashboard Handler] Listening for dashboards on {host}:{port}")
            
            while True: 
                conn, addr = s.accept()
                print(f"[Dashboard Handler] Dashboard connected from {addr}")
                connected_dashboards.append(conn)
   
    thread = threading.Thread(target=listener, daemon=True)
    thread.start()
   
def broadcast_to_dashboards(message):
    for dash_conn in connected_dashboards[:]:
        try:
            dash_conn.sendall((message + "\n").encode('utf-8'))
        except Exception as e:
            connected_dashboards.remove(dash_conn)