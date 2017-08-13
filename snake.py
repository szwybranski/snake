import sys, pygame, time
from random import randint

class Screen(object):
    def __init__(self, screen_width, screen_height, block_size):
        assert(screen_width % block_size == 0)
        assert(screen_height % block_size == 0)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block_size = block_size

    def get_screen_size(self):
        return (self.screen_width, self.screen_height)

    def get_block_size(self):
        return (self.block_size)

class Snake(object):
    def __init__(self, screen):
        self.left = 1
        self.right = 0
        self.up = 0
        self.down = 0
        self.screen = screen
        start_x = self.screen.get_screen_size()[0]/2 - (self.screen.get_screen_size()[0]/2) % self.screen.get_block_size()
        start_y = self.screen.get_screen_size()[1]/2 - (self.screen.get_screen_size()[1]/2) % self.screen.get_block_size()
        make_snake = lambda x: pygame.Rect(start_x + self.screen.get_block_size() * x, start_y, self.screen.get_block_size(), self.screen.get_block_size())
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

    def hit_wall(self):
        return (self.head().x < 0
                or self.head().x > self.screen.get_screen_size()[0]
                or self.head().y < 0
                or self.head().y > self.screen.get_screen_size()[1])

    def move_it(self, make_snake_longer):
        head = pygame.Rect.copy(self.head())
        if self.left: head.x -= self.screen.get_block_size()
        elif self.right: head.x += self.screen.get_block_size()
        elif self.up: head.y -= self.screen.get_block_size()
        elif self.down: head.y += self.screen.get_block_size()
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
            block_size = self.screen.get_block_size()
            screen_size = self.screen.get_screen_size()
            x = randint(0, screen_size[0] - block_size)
            x = x - x % block_size # snap to grid
            y = randint(0, screen_size[1] - block_size)
            y = y - y % block_size
            self.pos = pygame.Rect(x, y, block_size, block_size)

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

def is_game_over(snake):
    return snake.hit_wall() or snake.hit_itself()

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
    label = font.render(text, 0, (200, 200, 200))
    surface.blit(label, (0, 0))

def get_current_time():
    return int(round(time.time() * 1000))

def play_game():
    pygame.init()
    pygame.display.set_caption("snake")
    screen = Screen(600, 400, 10)
    surface = pygame.display.set_mode(screen.get_screen_size())
    prev_time = None
    snake = Snake(screen)
    food = Food(screen)
    game_over = False
    bg_red = 0
    text = ""
    frames = []
    game_speed = 0

    # main game loop
    while True:
        handle_event_loop(snake)
        current_time = get_current_time()
        if not prev_time or (current_time - prev_time > (50 - game_speed)):
            prev_time = current_time
            if not game_over:
                advance_game(snake, food)
                game_speed = min(food.get_total(), 20)
                game_over = is_game_over(snake)
            else:
                bg_red += 30
                if bg_red > 150: break

        # frame rendering
        surface.fill((bg_red, 0, 0))
        text = " score={}, fps={}, speed={}".format(food.get_total(), len(frames), game_speed)
        paint_text(surface, text)
        paint_snake(surface, snake)
        paint_food(surface, food)
        pygame.display.flip()

        # leave timestamps generated during last second, length of this array = fps
        frames = [ current_time ] + frames
        while frames and (current_time - frames[-1] > 1000): del frames[-1]

def main():
    while True:
        play_game()

if __name__ == "__main__":
    main()

