import socket 
import threading
import os, fnmatch   


HEADER = 64
PORT = 5050
# localhost, socket object
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
#  8-bit encoding ->  no byte ordering issues.
FORMAT = 'utf-8'
DISCONNECT = "DISCONNECT"

# IPv4 & TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind with address & port
server.bind(ADDR)


Accounts = {}
id_count = 0

def search(name):
    # This is to get the directory that the program 
    # is currently running in.
    dir_path = os.path.dirname(os.path.realpath("./accounts/"))
    pattern = name + ".txt"  
    
    for root, dirs, files in os.walk(dir_path):
        for file in files: 

            if fnmatch.fnmatch(file, pattern):
                f = open("accounts/"+file)
                acc_details = f.readline()
                return acc_details.split(), True

    return "ERROR", False

def write_to_file(client):
    temp = " "
    temp = temp.join(Accounts[client])
    details = client + " " + temp
    pattern = client + ".txt"
    with open("accounts/"+pattern, "w") as myfile:
            myfile.write(details)

def handle_client(conn, addr):
    
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    logged_in = False

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)

        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            

            msg = msg.split()
            action = msg[0].upper()

            if len(msg) < 2 and action != "BALANCE":
                conn.send(" ERROR, PLEASE TRY AGAIN ".encode(FORMAT))
                continue

            print("MESSAGE RECIEVED : ", msg)

            print("ACTION RECIEVED : ", action)
            
            if action == "DISCONNECT":
                print("DISCONNECTED") 
                connected = False

            elif action == "LOGIN":

                if len(msg) < 3:
                    conn.send(" ERROR WHILE LOGIN IN, PLEASE TRY AGAIN ".encode(FORMAT))

                client_name = msg[1].upper()
                client_pin = msg[2].upper()
                
                print("CLIENT NAME : ", client_name)
                print("CLIENT PIN : ", client_pin)

                acc_credential, found = search(client_name)

                if found:

                    if acc_credential[1] == client_pin:
                        logged_in = True
                        # Name, pin, balance
                        acc_details = [client_name, client_pin, acc_credential[2]]
                        # To make it easier for us, load everithing into a dictionary 
                        Accounts[acc_details[0]] = acc_details[1:]
                        welcome_msg = " LOGED IN SUCCESSFULLY, WELCOME " + client_name
                        conn.send(welcome_msg.encode(FORMAT))
                    
                    else:
                        conn.send(" ERROR WHILE LOGIN IN, PLEASE TRY AGAIN ".encode(FORMAT))
                else:
                    conn.send(" ERROR WHILE LOGIN IN, PLEASE TRY AGAIN ".encode(FORMAT))        

            elif action == "BALANCE":
                if logged_in:
                    balance = Accounts[client_name][1]
                    response = " YOUR ACCOUNT BALANCE IS " + balance
                    conn.send(response.encode(FORMAT))

                else:
                    conn.send(" NOT LOGGED IN, PLEASE LOGIN FIRST! ".encode(FORMAT))

            elif action == "DEPOSIT":  
                if logged_in:
                    amount = int(msg[1])

                    #Update balance
                    curr_balance = int(Accounts[client_name][1])
                    new_balance = str(curr_balance + amount)
                    Accounts[client_name][1] = new_balance
                    # Write to the file  
                    write_to_file(client_name)
                    response = " YOUR NEW ACCOUNT BALANCE IS " + new_balance
                    conn.send(response.encode(FORMAT))

                else:
                    conn.send(" NOT LOGGED IN, PLEASE LOGIN FIRST! ".encode(FORMAT))
            
            elif action == "WITHDRAW":

                if logged_in:
                    amount = int(msg[1])
                    curr_balance = int(Accounts[client_name][1])
                    # Check Founds
                    if amount > curr_balance:
                        conn.send(" NOT ENOUGH FOUNDS ".encode(FORMAT))
                    else:
                        # Update balance   
                        new_balance = str(curr_balance - amount)
                        Accounts[client_name][1] = new_balance
                        try:
                            write_to_file(client_name)
                        except:
                            response = " ERROR TRY AGAIN" + new_balance
                            conn.send(response.encode(FORMAT))
                        else:    
                            # Send back new info
                            response = " YOUR ACCOUNT BALANCE IS " + new_balance
                            conn.send(response.encode(FORMAT))
                else:
                    conn.send(" NOT LOGGED IN, PLEASE LOGIN FIRST! ".encode(FORMAT))

            elif action == "TRANSFER":

                if len(msg) < 3:
                    conn.send(" ERROR, PLEASE TRY AGAIN ".encode(FORMAT))


                if logged_in:

                    # Amount to tranfer
                    amount = int(msg[1])
                    curr_balance = int(Accounts[client_name][1])
                    if amount > curr_balance or amount < 1:
                        conn.send(" NOT ENOUGH FOUNDS ".encode(FORMAT))
                    # Info about intended target    
                    target = msg[2].upper()
                    # Search for target 
                    target_details, found = search(target)
                    # If target found 
                    if found :
                        target_name = target_details[0]
                        Accounts[target_name] = target_details[1:]
                        # Update our balance
                        new_balance = str(curr_balance - amount)
                        Accounts[client_name][1] = new_balance
                        write_to_file(client_name)
                        # Update target details
                        target_balance = int(Accounts[target_name][1])
                        new_target_balance = target_balance + amount 
                        Accounts[target_name][1] = str(new_target_balance)
                        write_to_file(target_name)
                        conn.send(" TRANSANCTION SUCCEDED ".encode(FORMAT))
                
                    else:
                        conn.send(" ERROR IN TRANSACTION; PLEASE TRY AGAIN ")                
                
                       
        else:
            print("DISCONNECTED")
            connected = False
    # Close the connection if we have not recieved nothing     
    conn.close()
        

def start():
    # Enables the server to accept connections, no need for backlog this time
    server.listen()

    #
    # Threats are used due to "blocking" calls e.g. accept(), connect(), send(), and recv()
    #

    print(f"[LISTENING] Server is listening on {SERVER}")

    # Loop over blocking calls
    while True:
        # new socket object used to communicate to the client 
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

start()