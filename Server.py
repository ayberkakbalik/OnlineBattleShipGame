# AYBERK AKBALIK - S012309
# ARDA SÜMBÜL - S014593
import random
import sys
import time

from socket import *
from this import s

global host
global port
# global s


""" We initialized socket as s and we specified host and port. We initialize the server with particular host and port. 
We specified number of clients to access this port. Lastly, we accept connection from client and return connection. """
def initialize_server():                         
    s = socket(AF_INET,SOCK_STREAM)
    host = ''
    port = 34000                                 
    s.bind((host,port))
    s.listen(1)
    conn, addr = s.accept()

    return conn

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
alphabet2 = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9}   # For the numerical equivalent of the letters in the table. For example, when A5 is entered, it will go to the row at index 0 in the game table.
numbers = ["1","2","3","4","5","6","7","8","9","0"]
grid = [[]]
grid_size = 10
numberOfHitsToOpponent = 0
numberOfHitsToMe = 0

""" In this method, the game table which has 10x10 size is created. 
'#' is added for each point. '#' means empty zones."""
def create_board():
    global grid
    global grid_size
    rows,columns = (grid_size,grid_size)

    grid = []
    for i in range(rows):
        row = []
        for j in range(columns):
            row.append("#")
        grid.append(row)
    return grid


"""In print_board() method, we print the game table which was created create_board method. 
Also, letters for rows and numbers for columns are added. 
Thus, the coordinates can be followed more easily."""
def print_board(a):
    global alphabet
    print("+ ", end=" ")
    for numbers in range(10):                # For the numbers at top
        print(str(numbers), end=" ")
    print("")    

    for row in range(len(a)):
        print( alphabet[row], end="| ")      # For the numbers at top
        for col in range(len(a[row])):
            print(a[row][col],end=" ")
        print("")
    print("\n")


"""In the send_coordinates() method, the server is asked to enter the coordinates of the point in the opponent's table that he/she wants to shoot.
This information is sent from the server to the client. 
If an input other than the letters or numbers specified as valid is entered for the coordinate point, 
A warning message appears and valid coordinate points are requested to be entered."""
coordinates1 = ""
def send_coordinates() :
    global coordinates1
    cmd = input("Enter the coordinates: ")
    while not(cmd[0:1] in alphabet) or len(cmd) != 2 or not(cmd[1:2] in numbers) or gridopponent[int(alphabet2.get(cmd[0:1]))][int(cmd[1:2])] == "H" or gridopponent[int(alphabet2.get(cmd[0:1]))][int(cmd[1:2])] == "M":
        cmd = input("Warning! Invalid value or previously entered coordinates...." "\n" + "\nPlease enter valid coordinates: ")


    if cmd == 'quit':
        conn.close()
        sys.exit()

    if len(str.encode(cmd))>0:
        conn.send(str.encode(cmd))
        coordinates1 = cmd


"""After the coordinates where the server shoots are checked in the client, the information comes to this method. 
If the shot is successful, the 'H', which means 'Hitted', is placed on the opponent's table. 
Otherwise, 'M', which means 'Missed', is placed on the opponent's table.
If the number of 'H' reaches to 14, that means all the ships of the opponent are sunk. Player 1 (server) wins. Player 2 (client) loses. """
def receive_hit_or_not():
    global numberOfHitsToOpponent
    true_or_false = str(conn.recv(1024), "utf-8")
    if true_or_false == "True":
        print("You HIT the Player 2's ship!!!!! :)")
        numberOfHitsToOpponent += 1
        gridopponent[int(alphabet2.get(coordinates1[0:1]))][int(coordinates1[1:2])] = "H"
        if numberOfHitsToOpponent == 14:
            print("YOU WIN!")
            conn.close()
            sys.exit()
    elif true_or_false == "False":
        print("You MISSED the Player 2's ship :(")
        gridopponent[int(alphabet2.get(coordinates1[0:1]))][int(coordinates1[1:2])] = "M"

    print("Player 2's turn. Please wait...")

"""The coordinates where the client shoots are sent there and checked in receive_coordinates() method. 'B', 'C', 'D' and 'S' shows the ships.
If the client's shot is successful, the 'H', which means 'Hitted', is placed on the server's table.
Otherwise, 'M', which means 'Missed', is placed on the opponent's table.
If the number of 'H' reaches to 14, that means all the ships of the server are sunk. Player 1 (server) loses. Player 2 (client) wins. """
def receive_coordinates():
    global numberOfHitsToMe
    try:
        
        input_data = str(conn.recv(1024), "utf-8")
        print("Coordinates determined by the Player 2: "+ input_data)
        shipCoordinates = gridme[int(alphabet2.get(input_data[0:1]))][int(input_data[1:2])]
        if shipCoordinates == "B" or shipCoordinates == "C" or shipCoordinates == "D" or shipCoordinates == "S":
            print("Player 2 hit! :(")
            numberOfHitsToMe += 1
            gridme[int(alphabet2.get(input_data[0:1]))][int(input_data[1:2])] = "H"
            conn.send(str.encode("True"))
            if numberOfHitsToMe == 14:
                print("YOU LOSE!")
                conn.close()
                sys.exit()
        else:
            print("Player 2 missed! :)")
            gridme[int(alphabet2.get(input_data[0:1]))][int(input_data[1:2])] = "M"
            conn.send(str.encode("False"))

    except:
        pass


"""Player1's name are sent to client."""
def sendName():
    conn.send(str.encode(Player1))


"""The opponent's name are received from client."""
opponentName = ""
def receiveName():

    global opponentName
    name2 = str(conn.recv(1024), "utf-8")
    opponentName = name2


def process():
    while True:
        sendName()
        receiveName()
        send_coordinates()
        receive_hit_or_not()
        receive_coordinates()
        print("\n        "+"Player 1")
        print("        " + Player1)
        print_board(gridme)
        print("        "+"Player 2")
        print("        " + opponentName)
        print_board(gridopponent)


"""Thanks to the ships() method, Carrier, Battleship, Submarine and Destroyer are placed respectively in the game table of Player 1. 
Random coordinates from the game table are used for this placement."""
def ships():
    global grid
    global sizeC, sizeB, sizeS, sizeD
    sizeC = 5    # For the Carrier's size
    sizeB = 4    # For the Battleship's size
    sizeS = 3    # For the Submarine's size
    sizeD = 2    # For the Destroyer's size
    shipCarrier()
    shipBattleship()
    shipSubmarine()
    shipDestroyer() 
    return gridme                                        
            
def shipCarrier():
    randomSizeC = random.randint(0,sizeC)         
    verticalorHorizontal = random.randint(0,1)    # For placing the ship vertical or horizontal. 0 is horizontal, 1 is vertical.
    order = random.randint(0,9)                   # We wrote this line to determine row or column number that the ship will place
    if(verticalorHorizontal == 0):
        for i in range(sizeC):
            gridme[order][randomSizeC + i] = "C"
    else:
        for i in range(sizeC):
            gridme[randomSizeC + i][order] = "C"

def shipBattleship():
    randomSizeB = random.randint(0,sizeB)
    verticalorHorizontal = random.randint(0,1)    # For placing the ship vertical or horizontal. 
    order = random.randint(0,9)                   # We wrote this line to determine row or column number that the ship will place

    for i in range(sizeB):                        # To check if there is a ship at these coordinates. If there is, then turn back to same method and take another random coordinates.
        if(verticalorHorizontal == 0):
            if gridme[order][randomSizeB + i] != "#":
                return shipBattleship()
        elif(verticalorHorizontal == 1):
            if gridme[randomSizeB + i][order] != "#":
                return shipBattleship()

    for i in range(sizeB):          
        if(verticalorHorizontal == 0):
            gridme[order][randomSizeB + i] = "B"
        else:
            gridme[randomSizeB + i][order] = "B"

def shipSubmarine():
    randomSizeS = random.randint(0,sizeS)
    verticalorHorizontal = random.randint(0,1)    # For placing the ship vertical or horizontal
    order = random.randint(0,9)                   # We wrote this line to determine row or column number that the ship will place

    for i in range(sizeS):                        # To check if there is a ship at these coordinates. If there is, then turn back to same method and take another random coordinates
        if(verticalorHorizontal == 0):
            if gridme[order][randomSizeS + i] != "#":
                return shipSubmarine()
        elif(verticalorHorizontal == 1):
            if gridme[randomSizeS + i][order] != "#":
                return shipSubmarine()

    for i in range(sizeS):
        if(verticalorHorizontal == 0):
            gridme[order][randomSizeS + i] = "S"
        else:
            gridme[randomSizeS + i][order] = "S"

def shipDestroyer():
    randomSizeD = random.randint(0,sizeD)
    verticalorHorizontal = random.randint(0,1)    # For placing the ship vertical or horizontal
    order = random.randint(0,9)                   # We wrote this line to determine row or column number that the ship will place

    for i in range(sizeD):                        # To check if there is a ship at these coordinates. If there is, then turn back to same method and take another random coordinates
        if(verticalorHorizontal == 0):
            if gridme[order][randomSizeD + i] != "#":
                return shipDestroyer()
        elif(verticalorHorizontal == 1):
            if gridme[randomSizeD + i][order] != "#":
                return shipDestroyer()
    
    for i in range(sizeD):
        if(verticalorHorizontal == 0):
            gridme[order][randomSizeD + i] = "D"
        else:
            gridme[randomSizeD + i][order] = "D"                               
                     

if __name__ == '__main__':
    print("\n\nHey there! Welcome to the Online Battleship Game.\n" + "Good luck!\n")
    gridme = create_board()
    gridopponent = create_board()
    gridme = ships()
    print("        "+"Player 1")
    print_board(gridme)
    print("        "+"Player 2")
    print_board(gridopponent)
    print("We are waiting for the client to connect...")
    conn = initialize_server()
    Player1 = input("The client are connected!\nPlease enter your name: ")
    process()

