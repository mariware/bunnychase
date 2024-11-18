import pygame
from network import Network
from player import Player

import pickle
test_player = Player(100, 100)
test_player.score = 50
serialized = pickle.dumps(test_player)
deserialized = pickle.loads(serialized)


pygame.font.init()
font = pygame.font.Font(None,26)

width = 1000
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

bg = pygame.image.load('bg.png')
bg1 = pygame.image.load('bg1.png')

# colors
WHITE = (255, 255, 255)
LIGHTGREEN = (86, 129, 69)
GREEN = (45, 74, 44)

def drawStartScreen():
    ''' This function draws the start screen with start and quit options. '''
    win.blit(bg1,(0,0))

    pygame.draw.rect(win, LIGHTGREEN, (width // 2 - 60, height // 2, 120, 40))
    start_text = font.render('Start', True, WHITE)
    win.blit(start_text,(width // 2 - start_text.get_width() // 2, height // 2 + 10))

    pygame.draw.rect(win, GREEN, (width // 2 - 60, height // 2 + 60, 120, 40))
    quit_text = font.render('Quit', True, WHITE)
    win.blit(quit_text,(width // 2 - quit_text.get_width() // 2, height // 2 + 70))

    pygame.display.update()

def drawQuitScreen():
    ''' This function draws the quit screen with restart and quit options. '''
    win.blit(bg1, (0, 0))

    # Draw Restart button
    pygame.draw.rect(win, LIGHTGREEN, (width // 2 - 60, height // 2, 120, 40))
    restart_text = font.render('Restart', True, WHITE)
    win.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 10))

    # Draw Quit button
    pygame.draw.rect(win, GREEN, (width // 2 - 60, height // 2 + 60, 120, 40))
    quit_text = font.render('Quit', True, WHITE)
    win.blit(quit_text, (width // 2 - quit_text.get_width() // 2, height // 2 + 70))

    pygame.display.update()

def reset_game():
    ''' This function resets the necessary variables for the game to restart. '''
    global p, start_ticks, game_over  # Use global variables for reset.
    p = n.getP()  # Reset the player object.
    start_ticks = pygame.time.get_ticks()  # Reset the start time.
    game_over = False  # Reset the game over state.

def redrawWindow(win, players, current_player, time_left):
    ''' This function redraws to update the window with all players. '''
    win.blit(bg, (0, 0))
    for player in players:
        player.draw(win) # Draw each player in the list.
        
    score_text = font.render(f'Score: {current_player.score}', True, (255, 255, 255))
    win.blit(score_text, (10,10))
    
    timer_text = font.render(f'Time Left: {time_left}s', True, (255, 255, 255))
    win.blit(timer_text, (10, 40))

    pygame.display.update()

def main():
    running = True
    start_screen = True
    global n, p
    n = Network() # Initialize network connection.
    p = n.getP() # Get the player's data from the server.

    clock = pygame.time.Clock()

    game_duration = 60  # Set countdown duration in seconds
    start_ticks = pygame.time.get_ticks()  # Record start time
    game_over = False

    while running:
        clock.tick(60)

        win.fill((0, 0, 0))

        if start_screen:
            drawStartScreen()  # Draw the start screen with buttons

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    # Check if the Start button is clicked
                    if width // 2 - 60 <= x <= width // 2 + 60 and height // 2 <= y <= height // 2 + 40:
                        start_screen = False  # Exit start screen and start game

                    # Check if the Quit button is clicked
                    elif width // 2 - 60 <= x <= width // 2 + 60 and height // 2 + 60 <= y <= height // 2 + 100:
                        running = False  # Exit the game
        
        elif game_over:
            drawQuitScreen()  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    # Check if Restart button is clicked
                    if width // 2 - 60 <= x <= width // 2 + 60 and height // 2 <= y <= height // 2 + 40:
                        reset_game()  
                        game_over = False  
                        start_ticks = pygame.time.get_ticks()  # Reset the timer

                    # Check if Quit button is clicked
                    elif width // 2 - 60 <= x <= width // 2 + 60 and height // 2 + 60 <= y <= height // 2 + 100:
                        running = False  # Quit the game

        else:
            # Calculate time left
            elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
            time_left = max(0, game_duration - elapsed_seconds)

            if time_left == 0 and not game_over:
                game_over = True  # Trigger the game over screen only once

            players = n.send(p)  # Send this player's position and get all players' positions back.

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

            p.move()  # Update this player's position.
            redrawWindow(win, players, p, time_left)  # Draw all players in the window.

main()