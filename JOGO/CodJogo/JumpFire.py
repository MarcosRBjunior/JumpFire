import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 300
WINDOWHEIGHT = 565
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
BACKGROUNDCOLOR2 = (255, 255, 255)
FPS = 15
BADDIEMINSIZE = 5
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 100
PLAYERMOVERATE = 55
PLAYERMOVERATE2 = 118

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('JumpFire')
#pygame.mouse.set_visible(False)

# Set up the fonts.
font = pygame.font.SysFont("Algerian", 40)
font2 = pygame.font.SysFont("Impact", 20)
fontfire=pygame.font.Font("fontfire.ttf", 20)
fontfire2=pygame.font.Font("fontfire.ttf", 10)


# Set up sounds.
gameOverSound = pygame.mixer.Sound('LostGame.wav')
pygame.mixer.music.load('JumpManMusic.wav')

# Set up images.
playerImage = pygame.image.load('bobrock.png')
playerRect = playerImage.get_rect()
playerRect2 = playerImage.get_rect()
baddieImage = pygame.image.load('fire.png')
NomeJogo = pygame.image.load('NomeJogo.JPG')
Telafundo = pygame.image.load('predio.JPG')

# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR2)
playerRect.topleft = (WINDOWWIDTH / 5000, WINDOWHEIGHT - 700)
windowSurface.blit(NomeJogo, playerRect)
drawText('', font, windowSurface, (WINDOWWIDTH / 5), (WINDOWHEIGHT / 3.5))
drawText('', font, windowSurface, (WINDOWWIDTH / 2.5) - 30, (WINDOWHEIGHT / 2) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    # Set up the start of the game.
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 13, WINDOWHEIGHT - 70)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # The game loop runs while the game part is playing.
        score += 1 # Increase score.

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where to the cursor.
                '''playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]'''
        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        }

            baddies.append(newBaddie)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE2)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE2)

        # Move the baddies down.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # Delete baddies that have fallen past the bottom.
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)
        windowSurface.blit(Telafundo, playerRect2)
        windowSurface.blit(playerImage, playerRect)
        playerRect2.topleft = (WINDOWWIDTH / 5000, WINDOWHEIGHT - 560)

        # Draw the score and top score.
        drawText('Score: %s' % (score), fontfire, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), fontfire, windowSurface, 10, 40)

        # Draw the player's rectangle.
        windowSurface.blit(playerImage, playerRect)
        # Draw each baddie.
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score # set new top score
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', fontfire, windowSurface, (WINDOWWIDTH / 4), (WINDOWHEIGHT / 3.1))
    drawText('Precione espaco para recomecar.', fontfire2, windowSurface, (WINDOWWIDTH / 2.6) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
