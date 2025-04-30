from server.hospital_server import hospital_server
from server.dashboard_handler import start_dashboard_listener

if __name__ == "__main__":
    start_dashboard_listener()
    hospital_server()