import socket
import threading
import sys
import os

HEADER = 2048
PORT = int(sys.argv[1])
SERVER = socket.gethostbyname(socket.gethostbyname("localhost"))
ADDR = (SERVER, PORT)
NOFILE = "FILE DOES NOT EXIST"
FORMAT = "utf-8"
DC = "GOODBYE"
COMMAND = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


# Starting our server and using threads in order to keep the server running for multiple clients
def start():
    server.listen()
    print(f"Server is [LISTENING] on {SERVER}\n")
    while True:
        conn, addr = server.accept()
        print(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[Connections currently Active] {threading.active_count() - 1}\n")


# This code allows us to print the current working directory by passing the CREATED CONNN
def list_files_in_current_directory(conn):
    # Here we are getting our current working directory to print out its content
    current_directory = os.getcwd()
    files_and_directories = os.listdir(current_directory)
    # Returns to the client all the files in the directory
    for item in files_and_directories:
        conn.send(f"{item}\n".encode(FORMAT))


# This code enables us to use the "Get" command in our current working dirrectory:
def get_file_content(conn, file_name):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, file_name)
    # the above code gives us the pile path needed

    # simple if and else to verify that the file does exit in the directory otherwise send the NOFILE str
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        return conn.send(f"{content}\n".encode(FORMAT))
    else:
        print("[ERROR] FILE DOES NOT EXIST")
        conn.send(NOFILE.encode(FORMAT))
        return None

def put_file_content(conn, filename):
    recieved_response = conn.recv(HEADER).decode(FORMAT)
    if recieved_response == NOFILE:
        print(NOFILE)
    else:
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, filename)
        with open(file_path, 'w') as file:
            file.write(recieved_response)
     


def handle_client(conn, addr):
    print(f"[New connection Incoming] {addr} has connected.\n")

    # keeping the connection alive with a while loop untill client enters quit
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        # checks for msg after the initial blank message that initiates the connection
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DC:
                connected = False
            print(f"[{ADDR}] has sent '{msg}'!")

            # if users enters ls command we print out whats in our CWD
            if msg == "ls":
                list_files_in_current_directory(conn)
            elif msg != "ls":
                COMMAND = msg.split()
                # checking if the first part of the sent command is get, if so implement the get_file
                # function
                if COMMAND[0] == "get":
                    get_file_content(conn, COMMAND[1])
                elif COMMAND[0] == "put":
                    put_file_content(conn, COMMAND[1]) 

    conn.close()


print("[STARTING] server starting.....")

start()