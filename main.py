import random # For generating random numbers
import sys # To exit the program
import pygame 
from pygame import * # Basic pygame imports

# Global variables
FPS = 32 
SCREENHEIGHT = 511
SCREENWIDTH = 289
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GAME_IMAGES = {}
GAME_SOUNDS = {}

def welcomeScreen():
    # Shows welcome screen

    while True:
        for event in pygame.event.get():
            # If user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses spacebar then start the game
            elif event.type == KEYDOWN and event.key == K_SPACE:
                return

            # Else keep showing the welcome screen
            else:
                SCREEN.blit(GAME_IMAGES['home'], (0,0)) 
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    HIGHSCORE = 0
    # Extract HIGHSCORE from highscore.txt
    with open("highscore.txt", "r") as f:
        HIGHSCORE = int(f.read())

    score = 0 # Initialize score
    playerx = int(SCREENWIDTH/2) # Position of player in x coordinate
    playery = int(SCREENHEIGHT/1.28) # Position of player in y coordinate
    playerVelX = 15 # Velocity with which player will move left and right
    ballAccY = 5 # Velocity with which ball will come towards the ground

    newBall = getRandomBall() # Generate the first random ball
    # Use a list(ballList) of dictionaries({'ballX' : newBall[0]['x'], 'ballY' : newBall[0]['y'], 'ballNum' : newBall[0]['ballNum']}) containing ball's x and y coordinate and ballNum to get random ball colours
    ballList = [{'ballX' : newBall[0]['x'], 'ballY' : newBall[0]['y'], 'ballNum' : newBall[0]['ballNum']}]    

    # Play game start sound
    GAME_SOUNDS['gameBg'].play()

    while True:
        for event in pygame.event.get():
            # If user wants to quit
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            # If user wants to move to the left
            if event.type == KEYDOWN and event.key == K_LEFT:
                if playerx > 0:
                    playerx -= playerVelX

            # If user wants to move to the right
            if event.type == KEYDOWN and event.key == K_RIGHT:
                if playerx < SCREENWIDTH - 50:
                    playerx += playerVelX

        # Change each ball's y coordinate available in ballList
        for ball in ballList:
            ball['ballY'] += ballAccY

        # If ball goes out of the screen height remove it from the ballList
        for ball in ballList:
            if ball['ballY'] > SCREENHEIGHT:
                ballList.pop(0)
                score += 1
                
                # If score becomes more than high score change it and write it in highscore.txt
                if score > HIGHSCORE:
                    HIGHSCORE = score

                    with open("highscore.txt", "w") as f:
                        f.write(str(HIGHSCORE))
        
        # Generate new balls if the first ball's y coordinate becomes more than 250(means ball crossed almost the half of the screen height)
        if ballList[0]['ballY'] % 250 == 0:
            newBall = getRandomBall()
            ballX = newBall[0]['x']
            ballY = newBall[0]['y']
            ballNum = newBall[0]['ballNum']
            newBall = {'ballX' : newBall[0]['x'], 'ballY' : newBall[0]['y'], 'ballNum' : newBall[0]['ballNum']}
            ballList.append(newBall)
        
        # Check for each ball whether the player has been hit by the ball or not
        for ball in ballList:
            crashTest = isCollide(ball['ballX'], ball['ballY'], playerx, playery)
            # If the player has been hit by the ball move back to the home screen
            if crashTest:
                GAME_SOUNDS['gameOver'].play()
                return
        
        # Blit game images
        SCREEN.blit(GAME_IMAGES['background'], (0,0))
        SCREEN.blit(GAME_IMAGES['player'], (playerx, playery))

        # Blitting all available balls
        for ball in ballList:
            SCREEN.blit(GAME_IMAGES['balls'][ball['ballNum']], (ball['ballX'], ball['ballY']))

        SCREEN.blit(GAME_IMAGES['scoreArea'], (0, 0))  
        
        # Blitting score
        scoreDigits = [int(x) for x in list(str(score))]
        scoreWidth = 0 # Width to adjust the digits
        for digit in scoreDigits:
            SCREEN.blit(GAME_IMAGES['numbers'][digit], ((70 + scoreWidth), 3))
            scoreWidth += GAME_IMAGES['numbers'][digit].get_width()

        # Blitting high score
        highScoreDigits = [int(x) for x in list(str(HIGHSCORE))]
        highScoreWidth = 0 # Width to adjust the digits
        for digit in highScoreDigits:
            SCREEN.blit(GAME_IMAGES['numbers'][digit], ((215 + highScoreWidth), 3))
            highScoreWidth += GAME_IMAGES['numbers'][digit].get_width()

        # If player's score becomes 10,20,30 and so on (multiples of 10) play the sound
        if score % 10 == 0 and score >= 10:
            GAME_SOUNDS['scoreEarned'].play()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def getRandomBall():
    # Generate random balls
    ballY = -40 # Ball's y coordinate by trial and error so that the ball will seem like coming from the sky
    ballyX = random.randrange(0, SCREENWIDTH - GAME_IMAGES['balls'][0].get_width()) # Generate ball's x coordinate between 0 to screenwidth - ball's width
    ballNum = random.randrange(0, 2) # To get random ball colours

    ballPosAndNum = [{'x':ballyX, 'y':ballY, 'ballNum':ballNum}]

    return ballPosAndNum

def isCollide(ballX, ballY, playerX, playerY):
    # Check for collision
    # Values are based on trial and error
    if ballY + 20  >= playerY  and (playerX - 30 <= ballX <= playerX + 40):
        return True
    else:
        return False


if __name__ == "__main__":
    # This will be the main point from where our game will start

    pygame.init() # Initialize all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Giraffe Survival By Mayank Jha")

    GAME_IMAGES['background'] = pygame.image.load('gallery/images/bg.png')

    GAME_IMAGES['scoreArea'] = pygame.image.load('gallery/images/score.png')

    GAME_IMAGES['home'] = pygame.image.load('gallery/images/home.png')

    GAME_IMAGES['player'] = pygame.image.load('gallery/images/player.png').convert_alpha()

    GAME_IMAGES['balls'] = (
        pygame.image.load('gallery/images/ball1.png').convert_alpha(),
        pygame.image.load('gallery/images/ball2.png').convert_alpha(),
        pygame.image.load('gallery/images/ball3.png').convert_alpha()
    )

    GAME_IMAGES['numbers'] = (
        pygame.image.load('gallery/images/0.png').convert_alpha(),
        pygame.image.load('gallery/images/1.png').convert_alpha(),
        pygame.image.load('gallery/images/2.png').convert_alpha(),
        pygame.image.load('gallery/images/3.png').convert_alpha(),
        pygame.image.load('gallery/images/4.png').convert_alpha(),
        pygame.image.load('gallery/images/5.png').convert_alpha(),
        pygame.image.load('gallery/images/6.png').convert_alpha(),
        pygame.image.load('gallery/images/7.png').convert_alpha(),
        pygame.image.load('gallery/images/8.png').convert_alpha(),
        pygame.image.load('gallery/images/9.png').convert_alpha()
    )

    GAME_SOUNDS['gameOver'] = pygame.mixer.Sound('gallery/sounds/gameOver.wav')
    GAME_SOUNDS['gameBg'] = pygame.mixer.Sound('gallery/sounds/gameBg.wav')
    GAME_SOUNDS['scoreEarned'] = pygame.mixer.Sound('gallery/sounds/scoreEarned.wav')

    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # Main game function
