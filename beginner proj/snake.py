 
import pygame
import random

pygame.init()

# ---------------- COLORS ----------------
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 200, 0)
bg_color = (40, 44, 52)   # Nice dark background

# ---------------- SCREEN ----------------
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# ---------------- GAME SETTINGS ----------------
snack_block = 20          # Bigger block size
snake_speed = 12

font = pygame.font.SysFont("comicsansms", 25)

# ---------------- FUNCTIONS ----------------
def score(value):
    text = font.render("Score: " + str(value), True, yellow)
    screen.blit(text, [10, 10])

def snake(block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, green, [x[0], x[1], block, block])

def message(msg, color):
    text = font.render(msg, True, color)
    screen.blit(text, [width / 6, height / 3])

# ---------------- MAIN GAME LOOP ----------------
def gameLoop():
    game_over = False
    game_close = False

    x1 = width // 2
    y1 = height // 2
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = random.randrange(0, width - snack_block, snack_block)
    foody = random.randrange(0, height - snack_block, snack_block)

    while not game_over:

        # -------- GAME OVER SCREEN --------
        while game_close:
            screen.fill(bg_color)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        # RESET GAME STATE (NO RECURSION)
                        x1 = width // 2
                        y1 = height // 2
                        x1_change = 0
                        y1_change = 0
                        snake_List = []
                        Length_of_snake = 1
                        foodx = random.randrange(0, width - snack_block, snack_block)
                        foody = random.randrange(0, height - snack_block, snack_block)
                        game_close = False

        # -------- EVENTS --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snack_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snack_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snack_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snack_block
                    x1_change = 0

        # -------- WALL COLLISION --------
        if x1 < 0 or x1 >= width or y1 < 0 or y1 >= height:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(bg_color)

        pygame.draw.rect(screen, red, [foodx, foody, snack_block, snack_block])
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # -------- SELF COLLISION --------
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        snake(snack_block, snake_List)
        score(Length_of_snake - 1)

        pygame.display.update()

        # -------- FOOD EAT --------
        if x1 == foodx and y1 == foody:
            foodx = random.randrange(0, width - snack_block, snack_block)
            foody = random.randrange(0, height - snack_block, snack_block)
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# ---------------- START GAME ----------------
gameLoop()
 