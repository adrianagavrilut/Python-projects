from tkinter import *
import random
import winsound
from pathlib import Path

# Define game constants
GAME_WIDTH = 700
GAME_HEIGHT = 600
SPEED = 55
SPACE_SIZE = 40
BODY_PARTS = 2
SNAKE_COLOR = "#00ff00"
FOOD_COLOR = "#e60000"
BACKGROUND_COLOR = "#121818"

working_dir = Path(__file__).absolute().parent

# Class representing the Snake in the game
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


# Class representing the Food in the game
class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        
        self.coordinates = [x, y]
        
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


# Function to handle the snake's next turn and movement
def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]: # if collision with food

        global score
        score += 1
        label.config(text="Score:{}".format(score))
        play_eat_sound()
        canvas.delete("food")
        food = Food()

    else:
        # delete last body part
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collision(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)


# Function to change the snake's direction based on user input
def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


# Function to check collision with walls or itself
def check_collision(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


# Function to handle the game over scenario
def game_over():
    play_game_over_sound()
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('Bell MT',50), text="GAME OVER", fill="red", tag="gameover")


# Function to restart the game
def restart_game():
    global snake, food, score, direction
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))
    next_turn(snake, food)


# Function for food eating sound
def play_eat_sound():
    winsound.PlaySound(working_dir/'bitee.wav', winsound.SND_ASYNC)

# Function for game over sound
def play_game_over_sound():
    winsound.PlaySound(working_dir/'death.wav', winsound.SND_ASYNC)


# Create the Tkinter window
window = Tk()
window.title("Snake game")
window.resizable(False, False)

# Create restart button
restart_button = Button(window, text="Restart", command=restart_game, font=('Bodoni MT', 20))
restart_button.place(x=10, y=5)

# Initialize score and direction
score = 0
direction = 'down'

# Create label to display score
label = Label(window, text="Score: {}".format(score), font=('Bodoni MT', 36))
label.pack()

# Create canvas for the game
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Get window dimensions and center it on the screen
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind arrow key presses to change direction
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Initialize snake and food objects
snake = Snake()
food = Food()

# Start the game loop
next_turn(snake, food)

# Run the Tkinter main loop
window.mainloop()