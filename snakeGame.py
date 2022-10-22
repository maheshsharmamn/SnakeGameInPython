import pygame
import random
import os

# initializing music
pygame.mixer.init()

# creating colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 200, 0)
yellow = (155, 255, 155)
black = (0, 0, 0)

pygame.init()
# creating game window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# for background image
bgimg = pygame.image.load("back.jpg")
bgimg = pygame.transform.scale(
    bgimg, (screen_width, screen_height)).convert_alpha()
pygame.display.set_caption("SnakeWithMahesh")
pygame.display.update()


# for showing score on screen
font = pygame.font.SysFont('constantia', 55)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

# for ploting snake


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


# for clock in pygame
clock = pygame.time.Clock()

# welcome screen


def welcome():
    exit_game = False
    while not exit_game:
        # gameWindow.fill((250,150,230))
        img = pygame.image.load("welcome.jpg")
        img = pygame.transform.scale(
            img, (screen_width, screen_height)).convert_alpha()
        gameWindow.blit(img, (0, 0))
        text_screen("Welcome to Snakes!", black, 250, 10)
        text_screen("Press Space!", black, 300, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameLoop()
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    quit()


# game loop
def gameLoop():
    pygame.mixer.music.load("back.mp3")
    pygame.mixer.music.play()
    # game specific variable
    exit_game = False
    game_over = False
    snake_x = 150
    snake_y = 150
    snake_size = 10

    init_velocity = 2
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    food_x = random.randint(20, screen_width/2)
    food_y = random.randint(20, screen_height/2)
    fps = 60
    score = 0
    if not os.path.exists("hiscore.txt"):
        with open("hiscore.txt", "w") as f:
            f.write("0")
    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    while not exit_game:
        if game_over:
            # gameWindow.fill(white)
            img = pygame.image.load("gameOver.jpg")
            img = pygame.transform.scale(
                img, (screen_width, screen_height)).convert_alpha()
            gameWindow.blit(img, (0, 0))
            text_screen("Score : " + str(score), red, 350, 10)
            text_screen("Press Enter to continue", green, 190, 320)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y
            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score += 10
                # print("Score :",score*10)
                food_x = random.randint(20, screen_width/2)
                food_y = random.randint(20, screen_height/2)
                snk_length += 3
                if score > int(hiscore):
                    hiscore = score
                    with open("hiscore.txt", "w") as f:
                        f.write(str(hiscore))

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            # showing score
            text_screen("Score : " + str(score) +
                        "  High Score :" + str(hiscore), yellow, 5, 5)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]
            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load("gameover.mp3")
                pygame.mixer.music.play()
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load("gameover.mp3")
                pygame.mixer.music.play()
                # print("game over")
            plot_snake(gameWindow, black, snk_list, snake_size)
            pygame.draw.rect(gameWindow, red, [
                             food_x, food_y, snake_size, snake_size])
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
gameLoop()
