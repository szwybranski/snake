import sys, pygame, time
from random import randint

class Screen(object):
    def __init__(self, block_width, block_height, screen_width, screen_height):
        self.block_width = block_width
        self.block_height = block_height
        self.screen_width = screen_width
        self.screen_height = screen_height

    def get_screen_size(self):
        return (self.screen_width, self.screen_height)

    def get_block_size(self):
        return (self.block_width, self.block_height)

class Snake(object):
    def __init__(self, screen):
        self.left = 1
        self.right = 0
        self.up = 0
        self.down = 0
        screen_size = screen.get_screen_size()
        self.width, self.height = screen.get_block_size()
        make_snake = lambda x: pygame.Rect(screen_size[0]/2+self.width*x, screen_size[1]/2, self.width, self.height)
        self.body = [ make_snake(0), make_snake(1), make_snake(2), make_snake(3), make_snake(4) ]

    def get_pos(self):
        return self.body

    def set_direction(self, left=0, right=0, up=0, down=0):
        self.left = left
        self.right = right
        self.up = up
        self.down = down

    def head(self):
        return self.body[0]

    def hit_itself(self):
        seen = set()
        for s in self.body:
            if (s.x,s.y) in seen: return True
            seen.update({(s.x,s.y)})
        return False

    def move_it(self, make_snake_longer):
        head = pygame.Rect.copy(self.body[0])
        if self.left: head.x -= self.width
        elif self.right: head.x += self.width
        elif self.up: head.y -= self.height
        elif self.down: head.y += self.height
        self.body = [head] + self.body
        if not make_snake_longer:
            del self.body[-1]

class Food(object):
    def __init__(self, screen):
        self.screen = screen
        self.pos = None
        self.total = 0

    def get_pos(self):
        return self.pos

    def exists(self):
        return self.pos != None

    def remove(self):
        self.pos = None
        self.total += 1
        
    def get_total(self):
        return self.total

    def place_if_missing(self):
        if not self.exists():
            width, height = self.screen.get_block_size()
            screen_size = self.screen.get_screen_size()
            x = randint(0, screen_size[0]-width)
            x = x - x % width # snap to grid
            y = randint(0, screen_size[1]-height)
            y = y - y % height
            self.pos = pygame.Rect(x, y, width, height)

def wall_hit(head, screen_size):
    return head.x < 0 or head.x > screen_size[0] or head.y < 0 or head.y > screen_size[1]

def snake_hit_food(head, food):
    return (head.x, head.y) == (food.x, food.y)

def handle_event_loop(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.set_direction(left=1)
            elif event.key == pygame.K_RIGHT:
                snake.set_direction(right=1)
            elif event.key == pygame.K_UP:
                snake.set_direction(up=1)
            elif event.key == pygame.K_DOWN:
                snake.set_direction(down=1)

def advance_game(snake, food):
    food.place_if_missing()
    make_snake_longer = False
    # check food and head collision
    if snake_hit_food(snake.head(), food.get_pos()):
        food.remove()
        make_snake_longer = True

    snake.move_it(make_snake_longer)                

def is_game_over(snake, screen_size):
    return wall_hit(snake.head(), screen_size) or snake.hit_itself()
    
def paint_snake(surface, snake):
    snake_color = (0, 204, 0)
    for s in snake.get_pos():
        pygame.draw.rect(surface, snake_color, s)

def paint_food(surface, food):
    if food.exists():
        food_color = (225, 49, 76)
        pygame.draw.rect(surface, food_color, food.get_pos())

def paint_text(surface, text):
    font = pygame.font.SysFont("verdana", 12)
    label = font.render(text, 0, (255, 255, 255))
    surface.blit(label, (0, 0))
        
def get_current_time():
    return int(round(time.time() * 1000))
    
def play_game():
    pygame.init()
    screen = Screen(10, 10, 600, 400)
    surface = pygame.display.set_mode(screen.get_screen_size())
    prev_time = None
    snake = Snake(screen)
    food = Food(screen)
    game_over = False
    bg_red = 0
    text = ""
    # main game loop
    while True:
        handle_event_loop(snake)
        current_time = get_current_time()
        if not prev_time or (current_time - prev_time > 50):
            prev_time = current_time
            if not game_over:
                advance_game(snake, food)
                text = "SCORE={}".format(food.get_total())
                if is_game_over(snake, screen.get_screen_size()):
                    game_over = True
                    text += " GAME OVER"
            else:
                bg_red += 30
                if bg_red > 150: break

        # frame rendering
        surface.fill((bg_red, 0, 0))
        paint_text(surface, text)
        paint_snake(surface, snake)
        paint_food(surface, food)
        pygame.display.flip()
    

def main():
    while True:    
        play_game()

if __name__ == "__main__":
    main()

