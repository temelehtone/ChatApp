from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time

#GLOBAL CONSTANTS
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
BUFSIZE = 512
FORMAT = "utf8"

class Client:
    # For communication with server
    def __init__(self, name):
        # Init object and send name to server

        self.name = name
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(ADDR)
        self.messages = []
        receive_thread = Thread(target=self.receive_message)
        receive_thread.start()
        self.send_message(name)
        self.lock = Lock()

    def set_name(self, name):
        self.name = name
    

    def receive_message(self):
    # Receive messages from server

        while True:
            try:
                msg = self.client_socket.recv(BUFSIZE).decode()
                # make sure memory is safe to access
                self.lock.acquire()
                self.messages.append(msg)
                print(self.messages)
                self.lock.release()

            except Exception as e:
                print("[EXCEPTION]", e)
                break


    def send_message(self, msg):
        # Send messages to server
        try:
            self.client_socket.send(bytes(msg, FORMAT))
            if msg == "{quit}":
                self.client_socket.close()
        except Exception as e:
            print(e)

    def get_messages(self):
        # Returns a list of messages
        messages_copy = self.messages[:]
        # make sure memory is safe to access
        self.lock.acquire()
        self.messages = []
        self.lock.release()
        return messages_copy

    def disconnect(self):
        self.send_message("{quit}")