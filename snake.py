from tkinter import *
import random

# Constants
game_width = 1200
game_height = 600
speed = 120
space_size = 30
body_parts = 3
snake_color = "#00FF00"
food_color = "#FF0000"
background_color = "#000000"

class Snake:
    def __init__(self):
        self.body = []
        self.direction = 'down'
        for i in range(body_parts):
            self.body.append([0, 0])

    def move(self):
        x, y = self.body[0]

        if self.direction == 'up':
            y -= space_size
        elif self.direction == 'down':
            y += space_size
        elif self.direction == 'left':
            x -= space_size
        elif self.direction == 'right':
            x += space_size

        new_head = [x, y]

        self.body = [new_head] + self.body[:-1]

    def grow(self):
        self.body.append(self.body[-1])

    def change_direction(self, new_direction):
        if new_direction == 'left' and self.direction != 'right':
            self.direction = new_direction
        elif new_direction == 'right' and self.direction != 'left':
            self.direction = new_direction
        elif new_direction == 'up' and self.direction != 'down':
            self.direction = new_direction
        elif new_direction == 'down' and self.direction != 'up':
            self.direction = new_direction

    def check_collision(self):
        x, y = self.body[0]
        if x < 0 or x >= game_width or y < 0 or y >= game_height:
            return True
        for segment in self.body[1:]:
            if x == segment[0] and y == segment[1]:
                return True
        return False

class Food:
    def __init__(self):
        self.position = self.new_position()

    def new_position(self):
        return [random.randint(0, (game_width // space_size) - 1) * space_size,
                random.randint(0, (game_height // space_size) - 1) * space_size]

    def respawn(self):
        self.position = self.new_position()

def handle_key(event):
    new_direction = event.keysym
    if new_direction in ['Left', 'Right', 'Up', 'Down']:
        snake.change_direction(new_direction.lower())

def update():
    snake.move()
    if snake.body[0] == food.position:
        global score
        score += 1
        label.config(text="Score: {}".format(score))
        snake.grow()
        food.respawn()

    if snake.check_collision():
        game_over()
    else:
        canvas.delete(ALL)
        draw_snake()
        draw_food()
        window.after(speed, update)

def draw_snake():
    for segment in snake.body:
        x, y = segment
        canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=snake_color)

def draw_food():
    x, y = food.position
    canvas.create_oval(x, y, x + space_size, y + space_size, fill=food_color)

def game_over():
    canvas.delete(ALL)
    canvas.create_text(game_width // 2, game_height // 2, text="GAME OVER", fill="red", font=('consolas', 70))

window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
snake = Snake()
food = Food()

label = Label(window, text="Score: {}".format(score), font=('consolas', 40))
label.pack()
canvas = Canvas(window, bg=background_color, height=game_height, width=game_width)
canvas.pack()

window.bind("<Key>", handle_key)

update()
window.mainloop()
