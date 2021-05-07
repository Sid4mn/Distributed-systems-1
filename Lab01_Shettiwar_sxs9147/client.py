import socket
import threading
import tkinter as tk
import os

# Global variables declared here 
IP = socket.gethostbyname(socket.gethostname())
PORT = 7669
SIZE = 1024
ADDR = (IP, PORT)
FORMAT= "utf-8"
CLIENT = socket.socket()
SEND_DIR = "client/send/" # The file to be sent will be sent from this folder
RECV_DIR = "client/recv/" # received file will be stored in this folder



def send(CLIENT,file_name):
    """This function is used to send the incorrect text data to the server"""
    # ref :https://realpython.com/read-write-files-python/
    while True:        
        filepath = SEND_DIR + file_name
        if os.path.exists(filepath) == False:
            msg.insert(tk.END, f"[ERROR] File not found: {filepath}")
        else:
            
            """ Reading the file text and sending it to the server. """           
            f = open(filepath, "r")
            data = f.read()
            msg.insert(tk.END,f"[SENDING] :{data}")
            CLIENT.send(data.encode(FORMAT))
            break
    

def receive(CLIENT,file_name):
   
    """This function is used to receive the corrected text data from the server"""
    while True:
        # ref :https://realpython.com/read-write-files-python/
        data = CLIENT.recv(SIZE).decode(FORMAT)              
        msg.insert(tk.END,f"[RECEIVED]:{data}")            
        if data :          
            save_path = RECV_DIR + file_name.replace(".txt","_corrected.txt")
            f = open(save_path, "w") #saving the data in path declared above
            f.write(data)
            f.close() 
            msg.insert(tk.END, f"[SUCCESS]Saved the updated file in: {save_path}")
            break
    
       
def clear_text(a,b) : # ref :https://stackoverflow.com/questions/2260235/how-to-clear-the-entry-widget-after-a-button-is-pressed-in-tkinter
    a.delete(0,'end')
    b.delete(0,'end')
    
    
def connect():
    #ref : https://stackoverflow.com/questions/34653875/python-how-to-send-data-over-tcp
    #ref : https://www.geeksforgeeks.org/socket-programming-python/
    """Checking user name and connecting to the server"""
    CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        CLIENT.connect(ADDR) #ref : https://www.networkcomputing.com/data-centers/python-network-programming-handling-socket-errors
    except socket.error:
        msg.insert(tk.END, "[ERROR]:connection error : make sure server is running, IP and port# are correct\n")
        exit(0)
    """ Getting inputs from the user"""
    #ref: https://www.geeksforgeeks.org/how-to-get-the-input-from-tkinter-text-box/
    user_name = str(entry_username.get())
    file_name = str(entry_filename.get())
    
    """If username entered is DISCONNECT the client connection is closed"""
    if user_name == "DISCONNECT":
            CLIENT.close()
            disconnect()
    else:
        CLIENT.send(user_name.encode(FORMAT))        
        connected = CLIENT.recv(SIZE).decode(FORMAT)
        
        """If username accepted by the server the following executes """
        if connected == "WELCOME" or connected == "Y":
            msg.insert(tk.END, "[SUCCESS] You are connected as " + user_name + ".\n")  # ref : https://www.python-course.eu/tkinter_message_widget.php 
            
            """Connect button to send the data to server """
            connect_button.configure(text="Disconnect", fg="Black", command=disconnect) 
            
            #ref : https://pythonguides.com/python-threading-and-multithreading/
            """Threading to send and receive data to/from multiple clients"""    
            threading.Thread(target=send, args=(CLIENT,file_name)).start()
            threading.Thread(target=receive, args=(CLIENT,file_name)).start()
            
            """Clearing input fields"""
            clear_text(entry_username,entry_filename)
            
            """If user clicks the disconnect button"""
            if disconnected_flag.get() == "N":
                disconnected_flag.set("1")
                
        #If username is rejected by the server
        else:
            msg.insert(tk.END, "Username: '" + user_name + "'already exists please enter a different username.\n")
    
    
def disconnect():
    """This function is used to disconnect from the server."""
    if disconnected_flag.get() == "1":
        disconnected_flag.set("Y")
    CLIENT.close()
    """Disconnect button"""
    connect_button.configure(text="Connect", fg="black", command=connect)
    msg.insert(tk.END, "You are not connected to the server.\n")


"""GUI for client code"""
window = tk.Tk() # Creating window
window.title("CLIENT GRAPHICAL USER INTERFACE") # ref: https://www.foxinfotech.in/2018/09/how-to-create-window-in-python-using-tkinter.html
frame = tk.Frame(window)

recv_file = tk.StringVar()
disconnected_flag = tk.StringVar()
disconnected_flag.set("N")

input1 = tk.Label(text="Enter a user Name")
input1.pack(side=tk.TOP) # ref : https://www.geeksforgeeks.org/how-to-get-the-input-from-tkinter-text-box/
input1.configure(bg="pink")
entry_username = tk.Entry(window)
entry_username.pack(side=tk.TOP)

input2 = tk.Label(text="Enter a File Name")
input2.pack(side=tk.TOP)
input2.configure(bg="pink")
entry_filename = tk.Entry(window)
entry_filename.pack(side=tk.TOP)
connect_button = tk.Button(window) # ref : https://www.pythontutorial.net/tkinter/tkinter-button/

connect_button.pack()

scrollbar = tk.Scrollbar(frame)  # To see old messages if any.
msg = tk.Listbox(frame, height=30, width=80, yscrollcommand=scrollbar.set) # Dimensions of the listbox
msg.configure(bg="turquoise") 
scrollbar.pack(side=tk.RIGHT, fill=tk.Y) # ref : https://www.geeksforgeeks.org/python-tkinter-scrollbar/
msg.pack(side=tk.LEFT, fill=tk.BOTH)
msg.pack()
frame.pack()

msg.insert(tk.END, "[WAITING FOR INPUT] CLIENT has started...\n")

threading.Thread(target=disconnect).start()

# Starts GUI execution.
tk.mainloop() # ref : https://stackoverflow.com/questions/29158220/tkinter-understanding-mainloop