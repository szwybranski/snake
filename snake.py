import sys, pygame, time
from random import randint
pygame.init()

size = (600, 400)
screen = pygame.display.set_mode(size)

# game colors
snake_color = pygame.Color(0, 204, 0)
food_color = pygame.Color(225, 49, 76)
bg_color = (0, 0, 0)

# defines snake and food size
width = 10
height = 10

# direction of the snake
left = 1
right = 0
up = 0
down = 0

# initial snake (5 rectangles)
snake = [ pygame.Rect(400+width*0, 300, width, height),
          pygame.Rect(400+width*1, 300, width, height),
          pygame.Rect(400+width*2, 300, width, height),
          pygame.Rect(400+width*3, 300, width, height),
          pygame.Rect(400+width*4, 300, width, height) ]

food = None
make_snake_longer = False
get_current_time = lambda: int(round(time.time() * 1000))
prev_time = get_current_time()
time_to_move = True

def move(l=0, r=0, u=0, d=0):
    global left, right, up, down
    left = l
    right = r
    up = u
    down = d

def wall_hit(head):
    return head.x < 0 or head.x > size[0] or head.y < 0 or head.y > size[1]

def snake_hit_itself(snake):
    seen = set()
    for s in snake:
        if (s.x,s.y) in seen: return True
        seen.update({(s.x,s.y)})
    return False

def snake_hit_food(head):
    return (head.x, head.y) == (food.x, food.y)

def handle_event_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move(l=1)
            elif event.key == pygame.K_RIGHT:
                move(r=1)
            elif event.key == pygame.K_UP:
                move(u=1)
            elif event.key == pygame.K_DOWN:
                move(d=1)

def move_snake():
    global snake, make_snake_longer
    head = pygame.Rect.copy(snake[0])
    if left: head.x -= width
    elif right: head.x += width
    elif up: head.y -= height
    elif down: head.y += height
    snake = [head] + snake
    if make_snake_longer:
        make_snake_longer = False
    else:
        del snake[-1]

def place_food():
    global food
    if not food:
       x = randint(0, size[0]-width)
       x = x - x % width # snap to grid
       y = randint(0, size[1]-height)
       y = y - y % height
       food = pygame.Rect(x, y, width, height)

def paint_snake():
    for s in snake:
        pygame.draw.rect(screen, snake_color, s)

def paint_food():
    if food:
        pygame.draw.rect(screen, food_color, food)

def advance_game():
    global food, make_snake_longer
    move_snake()
    place_food()

    # check food and head collision
    if snake_hit_food(snake[0]):
        food = None
        make_snake_longer = True

    # check for game over collisions
    if wall_hit(snake[0]) or snake_hit_itself(snake): sys.exit()

while True:
    handle_event_loop()

    current_time = get_current_time()
    if (current_time - prev_time > 50):
        prev_time = current_time
        advance_game()

    # frame rendering
    screen.fill(bg_color)
    paint_snake()
    paint_food()
    pygame.display.flip()
