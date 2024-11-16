import pickle
import socket
import time
from _thread import *
from player import Player
import sys
from ip_address import get_local_ip
import threading 

test_player = Player(100, 100)
test_player.score = 50
serialized = pickle.dumps(test_player)
deserialized = pickle.loads(serialized)

last_score_update = time.time()

server = get_local_ip()
port = 7000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Initialize socket.

try:
    s.bind((server, port)) # Bind server and port to socket.
except socket.error as e: # In case port is used, the server will not be bound.
    str(e)

s.listen(8) # Limit the number of clients.
print("Server started. It is waiting for a connection.")

# Initialize starting position of players.
players = [Player(150, 50), Player(250, 50), Player(350, 50), Player(450, 50), Player(550, 50), Player(650, 50), Player(750, 50), Player(850, 50)]
players[0].it = True
cooldown = 0
lock = threading.Lock()

def updateScores (players):
    '''To Continously increase the score of the bunny with carrot'''
    global last_score_update 
    current_time = time.time()
    
    if current_time - last_score_update >= 1:
        for player in players:
            if player.it:
                player.score += 1 
        last_score_update = current_time
        
def checkCollisions(players):
    ''' Handle collisions between players on the server side only. '''
    global cooldown
    current_time = time.time()

    for i, player1 in enumerate(players):
        rect1 = player1.hitbox

        for j, player2 in enumerate(players):
            if i != j:
                rect2 = player2.hitbox

                # Check if both players are eligible for a collision (cooldowns expired)
                if rect1.colliderect(rect2) and player1.it and current_time > cooldown:
                    # Transfer "it" status
                    player1.it = False
                    player2.it = True
                    player2.score += 10 #Add 10 spoints to those bunny/player who got the carrot
                    cooldown = current_time + 2  # Set 2-second cooldown
                    return players
    return players

def thread(conn, player):
    ''' This function handles each client thread. '''
    global players
    conn.send(pickle.dumps(players[player])) # Send player information to client.
    reply = ""

    while True: # Run this loop while client is connected.

        try: # Try to receive some data from client to ensure that connection is stable.
            data = pickle.loads(conn.recv(2048)) # Read player position.
            it = players[player].it
            players[player] = data # Update player position on server.
            players[player].it = it
            # If the data is not received properly, disconnect.
            if not data: 
                print("Disconnected.")
                break
            
            with lock:
                updateScores(players)

            # Send the updated list of all player information to the client.
            reply = checkCollisions(players)
            # print("Received from player", player, ":", data)
            # print("Sending to player", player, ":", reply)
            conn.sendall(pickle.dumps(reply))

        except: # End connection if there are other errors.
            break

    # If the connection is lost, close it.
    print("Connection lost.")
    conn.close()

currentPlayer = 0 # Set counter for number of players.

while True and currentPlayer <= 8: # Continuously wait for a connection.
    conn, addr = s.accept() # Accept incoming connection and store address.
    print("Connected to:", addr) # Print connection information.
    
    start_new_thread(thread, (conn, currentPlayer)) # Start a thread.
    currentPlayer += 1 # Add a new player.