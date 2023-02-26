import sys, random, os, time
import pygame as py

test = False
rigoler = False

#Gloabl variables
py.init()
py.mixer.init()
size = (600, 600)
screen = py.display.set_mode(size)
block_size = 40
clock = py.time.Clock()
speed = 7
FONT = py.font.Font(os.path.join('snake', 'font.ttf'), block_size*2)
rigole = py.image.load(os.path.join('snake', 'image.png'))

# Define colors
white = (150,150, 150)
red = (255, 0, 0)
green_yellow = (107,142,35)
green = (85,107,47)
black = (0,0,0)

#Sound
sound = py.mixer.Sound(os.path.join('snake', 'bruit.mp3'))

#Sprites
sprite = py.image.load(os.path.join('snake', 'snake-sprite.png'))
sprites = [sprite.subsurface((x%5)*64,(x//5)*64, 64, 64) for x in range(20)]

sprites_transform = []
for sprite in sprites:
    sprites_transform.append(py.transform.scale(sprite, (block_size, block_size)))

#Score
score = FONT.render('0', True, white)
score_rect = score.get_rect(center=(size[0] / 2, size[1] / 2))

def center_image(screen, image):
    screen.blit(image, (size[0] / 2 - image.get_width() / 2, size[1] / 2 - image.get_height() / 2))

def grid(screen):
    for x in range(0, size[0], block_size):
        py.draw.line(screen, white, (x, 0), (x, size[1]))
    for y in range(0, size[1], block_size):
        py.draw.line(screen, white, (0, y), (size[0], y))

def game_over(screen):
    image_1 = py.image.load(os.path.join('snake', 'gameover.png'))
    image = py.transform.scale(image_1, (400, 250))
    center_image(screen, image)





#Snake
class Snake:
    def __init__(self, screen_width, screen_height, screen):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.snake_surface = py.Surface((block_size, block_size))
        self.x_pos = (screen_width // block_size) // 4 * block_size
        self.y_pos = (screen_height // block_size) // 2 * block_size
        self.direction = "RIGHT"
        self.direction_x = 1
        self.direction_y = 0
        self.snake_body = [[self.x_pos, self.y_pos], [self.x_pos - block_size, self.y_pos]]
        self.game_over = False

    def show_snake(self, screen):
        #We print the queue of the snake
        #Queue to the down
        if self.snake_body[0][0] == self.snake_body[-2][0] and self.snake_body[0][1] == self.snake_body[-2][1] - block_size:
            screen.blit(sprites_transform[19], (self.snake_body[0][0], self.snake_body[0][1]))
        #Queue to the up
        elif self.snake_body[0][0] == self.snake_body[-2][0] and self.snake_body[0][1] == self.snake_body[-2][1] + block_size:
            screen.blit(sprites_transform[13], (self.snake_body[0][0], self.snake_body[0][1]))
        #Queue to the right
        elif self.snake_body[0][0] == self.snake_body[-2][0] + block_size and self.snake_body[0][1] == self.snake_body[-2][1]:
            screen.blit(sprites_transform[18], (self.snake_body[0][0], self.snake_body[0][1]))
        else:
            screen.blit(sprites_transform[14], (self.snake_body[0][0], self.snake_body[0][1]))


        #We change the body of the snake
        for i in range(1, len(self.snake_body)-1):
            #Sprite body straight to the top
            if self.snake_body[i][0] == self.snake_body[i-1][0] and self.snake_body[i][0] == self.snake_body[i+1][0]:
                screen.blit(sprites_transform[7], (self.snake_body[i][0], self.snake_body[i][1]))
                #py.draw.rect(self.screen, green_yellow, (body[0], body[1], block_size, block_size))
            #Sprite body straight to the right
            elif self.snake_body[i][1] == self.snake_body[i-1][1] and self.snake_body[i][1] == self.snake_body[i+1][1]:
                screen.blit(sprites_transform[1], (self.snake_body[i][0], self.snake_body[i][1]))
            #Angled sprite up to right
            elif self.snake_body[i][0] == self.snake_body[i+1][0] - block_size and self.snake_body[i][1] == self.snake_body[i-1][1] - block_size:
                screen.blit(sprites_transform[0], (self.snake_body[i][0], self.snake_body[i][1]))
            #Angled sprite up to right
            elif self.snake_body[i][0] == self.snake_body[i-1][0] - block_size and self.snake_body[i][1] == self.snake_body[i+1][1] - block_size:
                screen.blit(sprites_transform[0], (self.snake_body[i][0], self.snake_body[i][1]))
            #Angled sprite right to down
            elif self.snake_body[i][0] == self.snake_body[i-1][0] + block_size and self.snake_body[i][1] == self.snake_body[i+1][1] - block_size:
                screen.blit(sprites_transform[2], (self.snake_body[i][0], self.snake_body[i][1]))
            #Angled sprite down to left
            elif self.snake_body[i][0] == self.snake_body[i+1][0] + block_size and self.snake_body[i][1] == self.snake_body[i-1][1] - block_size:
                screen.blit(sprites_transform[2], (self.snake_body[i][0], self.snake_body[i][1]))
            #Angled sprite left to up
            elif self.snake_body[i][0] == self.snake_body[i-1][0] - block_size and self.snake_body[i][1] == self.snake_body[i+1][1] + block_size:
                screen.blit(sprites_transform[5], (self.snake_body[i][0], self.snake_body[i][1]))
            #Angled sprite down to right
            elif self.snake_body[i][0] == self.snake_body[i+1][0] - block_size and self.snake_body[i][1] == self.snake_body[i-1][1] + block_size:
                screen.blit(sprites_transform[5], (self.snake_body[i][0], self.snake_body[i][1]))
            #Angled sprite right to up
            elif self.snake_body[i][0] == self.snake_body[i-1][0] + block_size and self.snake_body[i][1] == self.snake_body[i+1][1] + block_size:
                screen.blit(sprites_transform[12], (self.snake_body[i][0], self.snake_body[i][1]))
            #Angled sprite left to up
            elif self.snake_body[i][0] == self.snake_body[i+1][0] + block_size and self.snake_body[i][1] == self.snake_body[i-1][1] + block_size:
                screen.blit(sprites_transform[12], (self.snake_body[i][0], self.snake_body[i][1]))



        #We change the head of the snake
        if self.direction == "RIGHT":
            screen.blit(sprites_transform[4], (self.snake_body[-1][0], self.snake_body[-1][1]))
            #py.draw.rect(self.screen, green, (self.snake_body[-1][0], self.snake_body[-1][1], block_size, block_size))
        elif self.direction == "LEFT":
            screen.blit(sprites_transform[8], (self.snake_body[-1][0], self.snake_body[-1][1]))
        elif self.direction == "UP":
            screen.blit(sprites_transform[3], (self.snake_body[-1][0], self.snake_body[-1][1]))
        else:
            screen.blit(sprites_transform[9], (self.snake_body[-1][0], self.snake_body[-1][1]))

    def body_add(self):
        self.snake_body.append([self.x_pos, self.y_pos])

    def check_exit(self):
        #Game Over if we exit of the screen
        if self.x_pos not in range(0, self.screen_width) or self.y_pos not in range(0, self.screen_height):
            self.game_over = True

    def check_body(self):
        #Game Over if we touch the body of the snake
        for body in snake.snake_body:
            if snake.x_pos == body[0] and snake.y_pos == body[1]:
                self.game_over = True

    def move(self):
        """ Function who change the coordinate of each blocks to follow the 'snake' """

        self.check_exit()

        HEAD = (self.x_pos, self.y_pos)
        self.snake_body.append(HEAD)
        for i in range(len(self.snake_body)-1):
            self.snake_body[i][0], self.snake_body[i][1] = self.snake_body[i+1][0], self.snake_body[i+1][1]
        self.x_pos += self.direction_x * block_size
        self.y_pos += self.direction_y * block_size
        self.snake_body.remove(HEAD)

        self.check_body()

#Items
class Items:
    def __init__(self, screen_widht, screen_height):
        self.screen_widht = screen_widht
        self.screen_height = screen_height
        self.items_surface = py.Surface((block_size, block_size))
        self.x_pos = (screen_widht // block_size) // 6* 5 * block_size
        self.y_pos = (screen_height // block_size) // 2 * block_size
        
    def show_items(self, screen):
        #py.draw.rect(screen, red, (self.x_pos, self.y_pos, block_size, block_size))
        screen.blit(sprites_transform[15], (self.x_pos, self.y_pos))
    def spawn_new_item(self, snake_body):
        x_pos = random.randrange(0, self.screen_widht, block_size)
        y_pos = random.randrange(0, self.screen_height, block_size)
    
        self.x_pos = x_pos
        self.y_pos = y_pos

snake = Snake(size[0], size[1], screen)
snake.show_snake(screen)

apple = Items(size[0], size[1])
apple.show_items(screen)

rigol = False

while True:

    for event in py.event.get():
        if event.type == py.QUIT:
            sys.exit()

        if event.type == py.KEYDOWN:
            if event.key == py.K_DOWN or event.key == py.K_s and snake.direction != "UP":
                snake.direction_x = 0
                snake.direction_y = 1
                snake.direction = "DOWN"
            if event.key == py.K_UP or event.key == py.K_z and snake.direction != "DOWN":
                snake.direction_x = 0
                snake.direction_y = -1
                snake.direction = "UP"
            if event.key == py.K_RIGHT or event.key == py.K_d and snake.direction != "LEFT":
                snake.direction_x = 1
                snake.direction_y = 0
                snake.direction = "RIGHT"
            if event.key == py.K_LEFT or event.key == py.K_q and snake.direction != "RIGHT":
                snake.direction_x = -1
                snake.direction_y = 0
                snake.direction = "LEFT"

    #Ce qu'il se passe lorque l'on passe sur une pomme
    if snake.x_pos == apple.x_pos and snake.y_pos == apple.y_pos:
        rigol = True
        if rigoler:
            sound.play()
        snake.body_add()
        apple.spawn_new_item(snake.snake_body)

    snake.move()
    
    # We update the score
    score = FONT.render(f"{len(snake.snake_body)-2}", True, white)

    screen.fill(black)

  
    screen.blit(score, score_rect)
    snake.show_snake(screen)
    apple.show_items(screen)

    if snake.game_over:
        screen.fill(black)
        game_over(screen)
        py.time.delay(300)
        snake = Snake(size[0], size[1], screen)
        apple = Items(size[0], size[1])
    
    if rigol and rigoler:
        center_image(screen, rigole)
        py.time.delay(200)
        rigol = False

    if test:
        screen.fill(black)
        center_image(screen, sprites[15])

    clock.tick(speed)
    py.display.flip()