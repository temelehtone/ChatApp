
from client import Client
import time
from threading import Thread


c1 = Client("Teuvo")
c2 = Client("Opa")




def update_messages():
    msgs = []

    while True:
        time.sleep(0.1) # Update every 100ms
        new_messages = c1.get_messages() # get any new messages from client 
        msgs.extend(new_messages) # add to local list of messages

        for msg in new_messages: # display new messages
            print(msg)
            if msg == "{quit}":
                break

Thread(target=update_messages).start()  



c1.send_message("hello")
time.sleep(4)
c2.send_message("whats uo")
time.sleep(4)
c1.send_message("nothing much")
time.sleep(4)
c2.send_message("nice to hear")
time.sleep(4)

c1.disconnect()
time.sleep(2)
c2.disconnect()