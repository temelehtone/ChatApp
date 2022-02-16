
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person


#GLOBAL CONSTANTS
HOST = "localhost"
PORT = 5500
BUFSIZE = 512
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
FORMAT = "utf8"

#GLOBAL VARIABLES 
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) # set up server

def broadcast(msg, name):
    # Send new messages to all clients

    for person in persons:
        client = person.client
        client.send(bytes(name + ": ", FORMAT) + msg)

def client_communication(person):
    # Thread to handle all messages from client
    
    client = person.client 
    addr = person.addr

    # First message received is always the persons name
    name = client.recv(BUFSIZE).decode(FORMAT)
    person.set_name(name)
    msg = bytes(f"{name} has joined the chat!", FORMAT)
    broadcast(msg, "") # Broadcasts welcome message
    
    while True: # Wait for any messages from person
        try:
            msg = client.recv(BUFSIZE)

            if msg == bytes("{quit}", FORMAT): # If message is quit disconnect client
                client.close()
                persons.remove(person)
                broadcast(bytes(f"{name} has left the chat...", FORMAT), "")
                
                print(f"[DISCONNECTED] {name} diconnected")
                break
            else:
                broadcast(msg, name + ": ")
                print(f"{name}: ", msg.decode(FORMAT))
        except Exception as e:
            print("[EXCEPTION]", e)

def wait_for_connection():
    # Wait for connection from new clients, start new thread once connected
    
    while True:
        try:
            client, addr = SERVER.accept() # Wait for any new connections
            person = Person(addr, client) # Create new person for connection
            persons.append(person)
            print(f"[CONNECTION] {addr} commected to the server at {time.time()}")
            Thread(target=client_communication, args=(person, )).start()
        except Exception as e:
            print("[FAILURE]", e)
            break
    print("SERVER CRASHED")

if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS) # Open server to listen for connections
    print("[STARTED] Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close() 