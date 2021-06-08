import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):

    try:
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)

    except socket.error as err:
        print("NOPE ", err)

    print(client.recv(2048).decode(FORMAT))

while True:

    print("************************************************************")
    print("==========      WELCOME TO THE BANKING SYSTEM     ==============")
    print("************************************************************")
    print("==========     (a). Login To Account            ============")
    print("==========     (b). Withdraw a Money            ============")
    print("==========     (c). Deposit a Money             ============")
    print("==========     (d). Check Balance               ============")
    print("==========     (e). Transfer                    ============")
    print("==========     (f). Quit/Logout                 ============")
    print("************************************************************")

    choice = input(" WHAT DO YOU WANT TO DO TODAY, ENTER A LETTER FROM THE ABOVE MENU : ")

    if choice == "a":

        msg = "LOGIN "
        client_name = input(" ENTER FIRST NAME : ")
        client_pin = input(" ENTER PIN : ")
        
        msg += client_name
        msg += " "
        msg += client_pin
    
        send(msg)

    elif choice == "b":
        msg = "WITHDRAW "
        amount = input(" STATE AMOUNT TO WITHDRAW : ")
        msg += amount
        send(msg)
        
    elif choice == "c":
        msg = "DEPOSIT "
        amount = input(" STATE AMOUNT TO DEPOSIT : ")
        msg += amount
        send(msg)

    elif choice == "d":
        msg = "BALANCE"
        send(msg)

    elif choice == "e":
        msg = "TRANSFER "
        amount = input(" PLEASE STATE THE AMOUNT TO TRANSFER : ")
        target = input(" PLEASE STATE THE INTENDED TARGET : ")

        msg += amount
        msg += " "
        msg += target

        send(msg)

    elif choice == "f":
        print(" THANK YOU FOR USING OUR SERVICES, WELCOME BACK SOON!")
        break
    main_menu = input(" PLEASE PRESS THE 'ENTER' TO GO BACK TO MENU ")

send("DISCONNECT")