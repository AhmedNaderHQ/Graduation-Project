import socket
from face_recognition_module import FaceRecognition
from driver_monitoring_module import DriverMonitor
from firebase_conn import update_feature_state ,send_message

#############################################
# Constants for socket connection
HOST = 'raspberrypi.local'
PORT = 1234

# Constants for message types
STOP:    int = 0
PLAY:    int = 1
AWAKE:   int = 3
WARN:    int = 4  # sleeping or dead
NO_FACE: int = 5
FINISH:  int = 6

#############################################
client_socket = socket.socket()
client_socket.connect((HOST, PORT))

#############################################

dfr = FaceRecognition()
update_feature_state("DFR", "ON", "Face Recognition Started")
dfr.load_users_data()
dfr.run()
update_feature_state("DFR", "OFF", "Face Recognition Stopped")


if dfr.is_verified():
    client_socket.send(str(PLAY).encode())
    send_message("Driver verified successfully.")

    dms = DriverMonitor(client_socket)
    update_feature_state("DMS", "ON", "Monitoring started...")
    dms.run()   # while loop for monitoring driver state until stopped by (sleep or dead)
    update_feature_state("DMS", "OFF", "Monitoring stopped.")
    update_feature_state("TSR", "OFF", "Traffic Sign Recognition started...")

else:
    send_message("Unauthorized driver detected.")
    client_socket.send(str(STOP).encode())

print("🛑 Program terminated.")

client_socket.close()
