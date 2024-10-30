import pygame
from network import Network
from player import Player

width = 1000
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

bg = pygame.image.load('bg.png')

def redrawWindow(win, players):
    ''' This function redraws to update the window with all players. '''
    win.blit(bg, (0, 0))
    for player in players:
        player.draw(win) # Draw each player in the list.
    pygame.display.update()

def main():
    running = True
    n = Network() # Initialize network connection.
    p = n.getP() # Get the player's data from the server.

    clock = pygame.time.Clock()

    while running:
        clock.tick(60)
        players = n.send(p)  # Send this player's position and get all players' positions back.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        p.move()  # Update this player's position.
        redrawWindow(win, players)  # Draw all players in the window.

main()