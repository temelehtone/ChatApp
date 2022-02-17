from email import message
from flask import Flask, render_template, session, url_for, request, redirect
from client import Client
from threading import Thread
import time

NAME_KEY = 'name'

app = Flask(__name__)
app.secret_key = "helloimteuvo"

client = None

def disconnect():
    global client
    if client:
        client.disconnect()

@app.route("/login", methods=["POST", "GET"])
def login():
    disconnect()
    if request.method == "POST":
        session[NAME_KEY] = request.form["inputName"]
        
        return redirect(url_for("home"))
    return render_template("login.html", **{"session": session})


@app.route("/logout")
def logout():
    disconnect()
    session.pop(NAME_KEY, None)
    return redirect(url_for("login"))


@app.route("/")
@app.route("/home")
def home():
    global client
    if NAME_KEY not in session:
        return redirect(url_for("login"))
    
    client = Client(session[NAME_KEY])
    return render_template("index.html", **{"login":True, "session": session})

@app.route("/send_message", methods=["GET"])
def run():
    
    global client

    msg = request.args.get("val")
    if client:
        client.send_message(msg)
        print(session["messages"])
        return render_template("index.html", **{"login":True, "session": session, "messages": session["messages"]})
    return "none"
   
def update_messages():
    global client
    while True:
        time.sleep(0.1) # Update every 100ms
        if not client: continue
        new_messages = client.get_messages() # get any new messages from client 
        session["messages"].extend(new_messages) # add to local list of messages
        
        for msg in new_messages: # display new messages
            if msg == "{quit}":
                break


if __name__ == "__main__":
    app.run(debug=True)
    Thread(target=update_messages).start() 