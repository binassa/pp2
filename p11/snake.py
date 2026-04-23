import turtle
import time
import random

delay = 0.1

# Score
score = 0
high_score = 0
coin_count = 0

# Food timer
food_lifetime = 8
food_spawn_time = time.time()

# Coin types
coin_types = {
    "bronze": 1,
    "silver": 3,
    "gold": 5
}

coin_colors = {
    "bronze": "brown",
    "silver": "lightgray",
    "gold": "gold"
}

# Screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("aquamarine")
wn.setup(width=600, height=600)
wn.tracer(0)

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.penup()

segments = []

# Random coin type
current_coin = "bronze"

# Function to spawn food
def spawn_food():
    global food_spawn_time, current_coin

    x = random.randint(-280, 280)
    y = random.randint(-280, 280)
    food.goto(x, y)

    current_coin = random.choice(list(coin_types.keys()))
    food.color(coin_colors[current_coin])

    food_spawn_time = time.time()

# First food
spawn_food()

# Score display
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("coral")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0  Coins: 0",
          align="center", font=("Courier", 16, "normal"))

# Movement
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)

# Controls
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

# Game loop
while True:
    wn.update()

    # FOOD TIMER (disappears after 5 seconds)
    if time.time() - food_spawn_time > food_lifetime:
        spawn_food()

    # Border collision
    if abs(head.xcor()) > 290 or abs(head.ycor()) > 290:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        for s in segments:
            s.goto(1000, 1000)
        segments.clear()

        score = 0
        delay = 0.1

        pen.clear()
        pen.write(f"Score: {score}  High Score: {high_score}  Coins: {coin_count}",
                  align="center", font=("Courier", 16, "normal"))

    # Food collision
    if head.distance(food) < 20:
        spawn_food()

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)

        score += coin_types[current_coin]
        coin_count += 1

        delay = max(0.05, delay * 0.98)

        if score > high_score:
            high_score = score

        pen.clear()
        pen.write(f"Score: {score}  High Score: {high_score}  Coins: {coin_count}",
                  align="center", font=("Courier", 16, "normal"))

    # Move segments
    for i in range(len(segments) - 1, 0, -1):
        x = segments[i - 1].xcor()
        y = segments[i - 1].ycor()
        segments[i].goto(x, y)

    if segments:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    # Self collision
    for s in segments:
        if s.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"

            for seg in segments:
                seg.goto(1000, 1000)
            segments.clear()

            score = 0
            delay = 0.1

            pen.clear()
            pen.write(f"Score: {score}  High Score: {high_score}  Coins: {coin_count}",
                      align="center", font=("Courier", 16, "normal"))

    time.sleep(delay)

wn.mainloop()