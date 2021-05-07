"""
SIDDHANT SHETTIWAR 
1001879146
DISTRIBUTED SYSTEMS LAB ASSIGNMENT 1
"""

"""Video references used for this project :
   https://www.youtube.com/watch?v=l5WU7d49OGk&list=PLS1QulWo1RIZGSgRsn0b8w9uoWM1gHDpo
   https://www.youtube.com/watch?v=QYYiQjZLnfA
   https://www.youtube.com/watch?v=Lbfe3-v7yE0
   https://www.youtube.com/watch?v=pwfnejaWkLQ
   https://www.youtube.com/watch?v=6jteAOmdsYg
   https://www.youtube.com/watch?v=VMP1oQOxfM0
   https://www.youtube.com/watch?v=_lSNIrR1nZU
   https://www.youtube.com/watch?v=JoQLe8Ff3YE
   https://www.youtube.com/watch?v=Jl1xsH6MR1g
"""

import socket # to create socket and use various socket programming functions
import threading # to handle multi threading
import tkinter as tk #for GUI 
import time # to use sleep function 



IP = socket.gethostbyname(socket.gethostname()) # This handles the dynamic IP address, this function  returns IP address of the HOST. ref: https://pythontic.com/modules/socket/gethostbyname
PORT = 7669
ADDR = (IP, PORT) # IP and PORT are combined into a tuple for future references
SIZE = 1024
FORMAT = "utf-8" # We need to encode the data while sending and receiving from the clients and server.
clients = [] # global list of clients to get updates everytime a new client is pushed into it.
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR) # Bind the socket with a IP and PORT number.


def lexicon_check(data):
    """  This function takes the data from the client and compares it with the lexicon
    present in the lexicon.txt and returns the updated data"""
    lex_file = "server/lexicon.txt"
    
    with open(lex_file, "r") as f:
        lex_data = f.read()

    lex_data = lex_data.strip().split(" ") # ref : https://pythonexamples.org/python-split-string-by-space/
    data = data.strip().split(" ")

    updated_data = []
    for d in data:
        """if small letters/words of the user input text is found in lex data, true is returned """
        if d.lower() in lex_data:
            updated_data.append(f"[{d}]") # ref : https://www.tutorialspoint.com/python3/list_append.html
            
            """if letters/word of the user input text is found in lex data, true is returned """
        elif d in lex_data:
            updated_data.append(f"[{d}]")          ##########  
            
            """remaining text of the user input which wasnt found in lex returned and appended"""
        else:
            updated_data.append(d)

    updated_data = " ".join(updated_data)
    return updated_data

def handle_client(conn, addr):
    # This function is used to handle the client thread.
        # ref : https://www.tutorialspoint.com/python/time_sleep.htm
        time.sleep(3) #To demonstrate that multiple clients cant join with same username. 
        
        username = conn.recv(SIZE).decode(FORMAT)      
        
        """if the client enters "DISCONNECT" as username, the client is disconnected from the server and client connection is closed."""
        if username == "DISCONNECT": #Also the while loop is broken to stop server from asking for username recursively.
            msg.insert(tk.END,"[DISCONNECTING]: Got a disconnect request from client")
            msg.insert(tk.END,f"[ACTIVE CLIENTS] {threading.activeCount() - 3}")
            conn.close()
         
        else:  
            
            """Checking if the username exists in the client global list or not by using the check_username function previously defined."""
            if username in clients:
                msg.insert(tk.END,"user already exists")
                conn.send("Nope".encode(FORMAT))
        
            else :
                """Sending a message to the client if username is accepted"""
                conn.send("WELCOME".encode(FORMAT))
                msg.insert(tk.END,f"[RECEIVED NAME]: {username}")
                
                """Adding the username to clients list so that no other client can use the same username"""
                clients.append(username.lower())
                
                """Displaying umber of Active Clients."""
                msg.insert(tk.END,f"[ACTIVE CLIENTS] - {threading.activeCount() - 2}{clients}")
        
                """ Displaying the name of the connected user."""
                msg.insert(tk.END,f"[CONNECTED] Username: {username}.")
    
                """Receive the text file data from the client in utf-8 encoded form."""
                data = str(conn.recv(SIZE).decode(FORMAT))
                msg.insert(tk.END,f"Text file received - {username}: {data}")
    
                """ Get the updated data from the lexicon_check function previously defined."""
                updated_data = lexicon_check(data)
                
                msg.insert(tk.END,f"Updated text file - {username}: {updated_data}")
    
                """ Encode the updated data and send it back to the client."""
                updated_data = updated_data.encode(FORMAT)
                conn.send(updated_data)
                clients.remove(username)
 
def connect():

    SERVER.listen(5) # Will listen for atmax 5 connections in the queue more than that will be dropped 

    """Infine loop to handle infinte clients"""
    while True:     
        conn, addr = SERVER.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        
        


window = tk.Tk()
window.title("SERVER GRAPHIC USER INTERFACE")

frame=tk.Frame(window) # ref: https://www.foxinfotech.in/2018/09/how-to-create-window-in-python-using-tkinter.html
scrollbar = tk.Scrollbar(frame) # creating a window
msg = tk.Listbox(frame,height= 40, width = 80,yscrollcommand=scrollbar.set) #https://stackoverflow.com/questions/4318103/resize-tkinter-listbox-widget-when-window-resizes
msg.configure(bg="pink")

scrollbar.pack(side=tk.RIGHT,fill=tk.Y) # adding a scrollbar
msg.pack(side=tk.RIGHT, fill=tk.BOTH) # ref : https://www.educba.com/tkinter-scrollbar/
msg.pack()
frame.pack()

msg.insert(tk.END, f"[LISTENING] Server is listening on {IP}:{PORT}.")

connect_thread = threading.Thread(target=connect) #  thread to connect function defined above
connect_thread.start()

tk.mainloop()  # Starts GUI execution.
