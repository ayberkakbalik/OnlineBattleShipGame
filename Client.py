# AYBERK AKBALIK - S012309
# ARDA SÜMBÜL - S014593
import os
import struct
import subprocess
import sys
from socket import *
import random

"""We initialized socket as s and we specified host and port (host is the client's IPv4) and connected to socket with particular host and port."""
def initialize_client():
    s = socket(AF_INET, SOCK_STREAM)
    host = '192.168.0.11'
    port = 34000
    s.connect((host, port))

    return s


alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
alphabet2 = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9}
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
def print_board(grid):
    global alphabet

    print("+ ", end=" ")
    for numbers in range(10):                # For the numbers at top
        print(str(numbers), end=" ")
        #print( alphabet[numbers], end="|")
    print("")    

    for row in range(len(grid)):
        #print(str(row), end=" ")
        print( alphabet[row], end="| ")
        for col in range(len(grid[row])):
            print(grid[row][col],end=" ")
        print("")
    print("\n")


"""In the send_coordinates() method, the client is asked to enter the coordinates of the point in the opponent's table that he/she wants to shoot.
This information is sent from the client to the server. 
If an input other than the letters or numbers specified as valid is entered for the coordinate point, 
A warning message appears and valid coordinate points are requested to be entered."""
coordinates1 = ""
def send_coordinates():
    global coordinates1
    cmd = input("Enter the coordinates: ")
    while not(cmd[0:1] in alphabet) or len(cmd)!=2 or not(cmd[1:2] in numbers) or gridopponent[int(alphabet2.get(cmd[0:1]))][int(cmd[1:2])] == "H" or gridopponent[int(alphabet2.get(cmd[0:1]))][int(cmd[1:2])] == "M":
        cmd = input("Warning! Invalid value or previously entered coordinates...." "\n" + "\nPlease enter valid coordinates: ")

    if cmd == 'quit':
        s.close()
        sys.exit()
    if len(str.encode(cmd))>0:
        s.send(str.encode(cmd))
        coordinates1 = cmd


"""The coordinates where the server shoots are sent there and checked in receive_coordinates() method. 'B', 'C', 'D' and 'S' shows the ships.
If the server's shot is successful, the 'H', which means 'Hitted', is placed on the client's table.
Otherwise, 'M', which means 'Missed', is placed on the opponent's table.
If the number of 'H' reaches to 14, that means all the ships of the server are sunk. Player 2 (client) loses. Player 1 (server) wins. """
def receive_coordinates():
    global numberOfHitsToMe
    print("Player 1's turn. Please wait...")
    try:
        input_data = str(s.recv(1024),"utf-8")
        print("Coordinates determined by the Player 1: "+ input_data)
        shipCoordinates = gridme[int(alphabet2.get(input_data[0:1]))][int(input_data[1:2])]
        if shipCoordinates == "B" or shipCoordinates == "S" or shipCoordinates == "D" or shipCoordinates == "C":
            print("Player 1 hit! :(")
            numberOfHitsToMe += 1
            gridme[int(alphabet2.get(input_data[0:1]))][int(input_data[1:2])] = "H"
            s.send(str.encode("True"))
            if numberOfHitsToMe == 14:
                print("YOU LOSE!")
                s.close()
                sys.exit()
        else:
            print("Player 1 missed! :)")
            gridme[int(alphabet2.get(input_data[0:1]))][int(input_data[1:2])] = "M"
            s.send(str.encode("False"))
    except:
        pass


"""After the coordinates where the client shoots are checked in the server, the information comes to this method. 
If the shot is successful, the 'H', which means 'Hitted', is placed on the opponent's table. 
Otherwise, 'M', which means 'Missed', is placed on the opponent's table.
If the number of 'H' reaches to 14, that means all the ships of the opponent are sunk. Player 2 (client) wins. Player 1 (server) loses. """
def receive_hit_or_not():
    global numberOfHitsToOpponent
    true_or_false = str(s.recv(1024), "utf-8")
    if true_or_false == "True":
        print("You HIT the Player 1's ship!!!! :)")
        numberOfHitsToOpponent += 1
        gridopponent[int(alphabet2.get(coordinates1[0:1]))][int(coordinates1[1:2])] = "H"
        if numberOfHitsToOpponent == 14:
            print("YOU WIN!")
            s.close()
            sys.exit()
    elif true_or_false == "False":
        print("You MISSED the Player 1's ship :(")
        gridopponent[int(alphabet2.get(coordinates1[0:1]))][int(coordinates1[1:2])] = "M"


"""The opponent's name are received from server."""
opponentName =""
def receiveName():
        global opponentName
        name2 = str(s.recv(1024), "utf-8")
        opponentName = name2


"""Player2's name are sent to server."""
def sendName():
        s.send(str.encode(Player2))

def process():
    while True:
        receiveName()
        sendName()
        receive_coordinates()
        send_coordinates()
        receive_hit_or_not()
        print("\n        "+"Player 2")
        print("        " + Player2)
        print_board(gridme)
        print("        "+"Player 1")
        print("        " + opponentName)
        print_board(gridopponent)


"""Thanks to the ships() method, Carrier, Battleship, Submarine and Destroyer are placed respectively in the game table of Player 2. 
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
    order = random.randint(0,9)                   # To determine row or column number that the ship will place
    if(verticalorHorizontal == 0):
        for i in range(sizeC):
            gridme[order][randomSizeC + i] = "C"
    else:
        for i in range(sizeC):
            gridme[randomSizeC + i][order] = "C"

def shipBattleship():
    randomSizeB = random.randint(0,sizeB)
    verticalorHorizontal = random.randint(0,1)    # For placing the ship vertical or horizontal. 
    order = random.randint(0,9)                   # To determine row or column number that the ship will place

    for i in range(sizeB):                        # To check if there is a ship at these coordinates. If there is, then turn back to same method and take another random coordinates
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
    order = random.randint(0,9)                   # To determine row or column number that the ship will place

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
    order = random.randint(0,9)                   # To determine row or column number that the ship will place

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
    print("        "+"Player 2")
    print_board(gridme)
    print("        "+"Player 1")
    print_board(gridopponent)
    print("You are connected in a second...")
    s= initialize_client()
    Player2 = input("You are connected!\nPlease enter your name: ")
    process()

