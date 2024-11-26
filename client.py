import pygame
from network import Network
from player import Player

pygame.font.init()
font = pygame.font.Font('font1.TTF', 20)

width = 1000
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

bg = pygame.image.load('bg.png')
bg1 = pygame.image.load('bg1.png')
bgwin = pygame.image.load('bgwin.png')
bglose = pygame.image.load('bglose.png')
fg1 = pygame.image.load('fg1.png')
fg2 = pygame.image.load('fg2.png')
fg3 = pygame.image.load('fg3.png')

# Initialize colors.
WHITE = (255, 255, 255)
LIGHTGREEN = (86, 129, 69)
GREEN = (45, 74, 44)
BLACK = (38, 23, 13)

def drawStartScreen():
    ''' This function draws the start screen with start and quit options. '''
    win.blit(bg1, (0,0))

    # Draw Start button.
    win.blit(fg2, (width // 2 - 60, height // 2))
    start_text = font.render('Start', True, BLACK)
    win.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2 + 33))

    # Draw Quit button.
    win.blit(fg2, (width // 2 - 60, height // 2 + 85))
    quit_text = font.render('Quit', True, BLACK)
    win.blit(quit_text,(width // 2 - quit_text.get_width() // 2, height // 2 + 118))

    pygame.display.update()

def drawNamePrompt():
    '''Draws a prompt to ask the player for their name.'''
    input_active = True
    name = ""
    input_box = pygame.Rect(0, 0, 300, 50)  # Initial box with default size
    input_box.center = (width // 2, height // 2)  # Center the box initially

    while input_active:
        win.blit(bg, (0, 0))
        
        # Render and center the prompt text
        prompt_text = font.render("Enter Name:", True, (0, 0, 0))
        win.blit(prompt_text, (width // 2 - prompt_text.get_width() // 2, height // 2 - 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        # Adjust the input box width dynamically based on text length
        text_surface = font.render(name, True, (0, 0, 0))
        input_box.h = text_surface.get_height() + 20
        input_box.w = text_surface.get_width() + 20  # Padding of 10 on each side
        input_box.center = (width // 2, height // 2 - 50)  # Keep the box centered

        # Draw the input box and text
        pygame.draw.rect(win, (0, 0, 0), input_box, 2)
        win.blit(text_surface, (input_box.x + 10, input_box.y + 10))  # Padding for text

        pygame.display.flip()

    return name
                    
    
def drawQuitScreen(final_score=None, winner=False):
    ''' This function draws the quit screen with restart and quit options. '''
    win.blit(bg1, (0, 0))
    
    #Display if the player won or lost.
    large_font = pygame.font.Font('font1.TTF', 90)
    if winner:
        win.blit(bgwin, (0, 0))
    else:
        win.blit(bglose, (0, 0))

    # Draw Restart button.
    win.blit(fg2, (width // 2 - 60, height // 2))
    restart_text = font.render('Restart', True, BLACK)
    win.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 33))

    # Draw Quit button.
    win.blit(fg2, (width // 2 - 60, height // 2 + 85))
    quit_text = font.render('Quit', True, BLACK)
    win.blit(quit_text, (width // 2 - quit_text.get_width() // 2, height // 2 + 118))

    pygame.display.update()

def reset_game():
    ''' This function resets the necessary variables for the game to restart. '''
    global p, start_ticks, game_over  # Use global variables for reset.
    p = n.getP()  # Reset the player object.
    start_ticks = pygame.time.get_ticks()  # Reset the start time.
    game_over = False  # Reset the game over state.

def redrawWindow(win, players, score, time_left):
    ''' This function redraws to update the window with all players. '''
    win.blit(bg, (0, 0))
    for player in players:
        player.draw(win) # Draw each player in the list.

    Player.draw_mini_cam(win, p)
    win.blit(fg3, (790, 390))

    win.blit(fg1, (20, 20))
    score_text = font.render(f'Score: {score}', True, BLACK)
    win.blit(score_text, (50, 53))
    timer_text = font.render(f'Time Left: {time_left}s', True, BLACK)
    win.blit(timer_text, (50, 73))

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

                    # Check if the Start button is clicked.
                    if width // 2 - 60 <= x <= width // 2 + 60 and height // 2 <= y <= height // 2 + 75:
                        player_name = drawNamePrompt()
                        p.name = player_name
                        start_screen = False  # Exit start screen and start game.

                    # Check if the Quit button is clicked.
                    elif width // 2 - 60 <= x <= width // 2 + 60 and height // 2 + 85 <= y <= height // 2 + 160:
                        running = False  # Exit the game.
        
        elif game_over:
            highest_score = max(player.score for player in players)
            is_winner = p.score == highest_score
            
            drawQuitScreen(final_score=p.score, winner=is_winner)  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    # Check if Restart button is clicked.
                    if width // 2 - 60 <= x <= width // 2 + 60 and height // 2 <= y <= height // 2 + 75:
                        reset_game()  
                        game_over = False  
                        start_ticks = pygame.time.get_ticks()  # Reset the timer.

                    # Check if Quit button is clicked
                    elif width // 2 - 60 <= x <= width // 2 + 60 and height // 2 + 85 <= y <= height // 2 + 160:
                        running = False  # Quit the game.

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

            # Update the local player's state based on the server data.
            for server_player in players:
                if server_player.id == p.id:  # Match player by ID.
                    p = server_player  # Update the local player's state.
                    break

            p.move()  # Update this player's position.
            redrawWindow(win, players, p.score, time_left)  # Draw all players in the window.

main()