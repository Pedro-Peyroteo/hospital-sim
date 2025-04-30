from server.hospital_server import hospital_server
from server.dashboard_handler import start_dashboard_listener, broadcast_thread_info
import threading

if __name__ == "__main__":
    print("[Hospital] Launching system from main.py")
    
    threading.Thread(target=broadcast_thread_info, daemon=True).start()
    print("[Hospital] broadcast_thread_info thread started")

    start_dashboard_listener(host='0.0.0.0', port=5999)
    print("[Hospital] Dashboard listener started")

    hospital_server()
