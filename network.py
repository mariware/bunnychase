import pickle
import socket
from ip_address import get_local_ip

class Network:
    def __init__(self):
        ''' This method initializes the network and confirms the connection. '''
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Initialize socket.
    #to try:    self.server = self.get_server_ip() 
        self.server = get_local_ip() # Initialize server.
        self.port = 7000 # Initialize port.
        self.addr = (self.server, self.port) # Bind the server and port to an address.
        self.p = self.connect() # Initialize connection and player.    

    #to try with other machine
    # def get_server_ip(self):
    #     ''' Retrieve the server IP address from a file or prompt the user '''
    #     try:
    #         with open("server_ip.txt", "r") as f:
    #             server_ip = f.read().strip()
    #             print(f"Server IP address found: {server_ip}")
    #             return server_ip
    #     except FileNotFoundError:
    #         server_ip = input("Enter the server's IP address: ").strip()
    #         return server_ip
    
    # or to try with  other machine 
    # def __init__(self):
    #     self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Initialize socket
    #     self.server = self.prompt_server_ip()  # Prompt for the server's IP address
    #     self.port = 7000
    #     self.addr = (self.server, self.port)
    #     self.p = self.connect()

    # def prompt_server_ip(self):
    #     ''' Prompt the user for the server's IP address '''
    #     while True:
    #         server_ip = input("Enter the server's IP address: ").strip()
    #         if self.validate_ip(server_ip):
    #             return server_ip
    #         print("Invalid IP address. Please try again.")

    # def validate_ip(self, ip):
    #     ''' Validate the entered IP address '''
    #     try:
    #         socket.inet_aton(ip)
    #         return True
    #     except socket.error:
    #         return False
    
        
    def connect(self):
        ''' This method attempts to connect to the server. '''
        try: # Try to connect to server.
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048)) # Load object data.
        except: # Pass if there are errors.
            pass

    def send(self, data):
        ''' This method sends some data to the server. '''
        try: # Send information to server.
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e: # Print an error if there is.
            print(e)
    
    def getP(self):
        ''' This method gets the player. '''
        return self.p