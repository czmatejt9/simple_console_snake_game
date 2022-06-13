# snake game using text
import shutil
import sys
import time
import cursor
from colorama import init
import keyboard
import random


class colors:
    line_home = "\033[H"
    screen_clear = "\033[J"
    reset='\033[0m'

    class bg:
        red='\033[41m'
        green='\033[42m'
        purple='\033[45m'


class Apple:
    def __init__(self, size, snake, color):
        self.x = random.randint(2, size.columns // 2)
        self.y = random.randint(2, size.lines)
        while (self.x, self.y) in snake.location:
            self.x = random.randint(2, size.columns // 2)
            self.y = random.randint(2, size.lines)
        move_cursor((self.x, self.y))
        sys.stdout.write(color+"  "+colors.reset)


class Snake:
    apple = None

    def __init__(self, width, height, color_head, color_body):
        self.location = list()
        self.color_head = color_head
        self.color_body = color_body
        self.direction = "right"
        self.score = 0
        for i in range(3):
            self.location.append((width // 2 - i, height // 2))
        for i, each in enumerate(self.location):
            x, y = each
            move_cursor((x, y))
            if i == 0:
                sys.stdout.write(self.color_head+"  "+colors.reset)
            else:
                sys.stdout.write(self.color_body+"  "+colors.reset)
        self.location.reverse()

    def move(self, size, apple_location: tuple, speed):
        head = self.location[-1]
        if self.direction == "right":
            x, y = head
            x += 1
            if x > size.columns // 2:
                x -= size.columns // 2
            self.location.append((x, y))
        elif self.direction == "left":
            x, y = head
            x -= 1
            if x < 1:
                x += size.columns // 2
            self.location.append((x, y))
        elif self.direction == "up":
            x, y = head
            y -= 1
            if y < 2:
                y += size.lines - 1
            self.location.append((x, y))
        elif self.direction == "down":
            x, y = head
            y += 1
            if y > size.lines:
                y -= size.lines - 1
            self.location.append((x, y))
        else:
            raise Exception("invalid direction was given")
        if not self.location[-1] == apple_location:
            move_cursor(self.location.pop(0))
            sys.stdout.write("  ")
        else:
            del self.apple
            self.score += speed
            move_cursor((10, 1))
            sys.stdout.write(f"Score: {self.score}")
            self.apple = Apple(size, self, colors.bg.green)

        move_cursor(self.location[-2])
        sys.stdout.write(self.color_body+"  "+colors.reset)
        move_cursor(self.location[-1])
        sys.stdout.write(self.color_head+"  "+colors.reset)
        move_cursor((20, 1))
        sys.stdout.write(str(self.location[-1])+"___")

    def collision(self):
        if len(self.location) != len(set(self.location)):
            return True
        else:
            return False


def move_cursor(coordinates: tuple):
    x, y = coordinates
    x = x * 2 - 1
    sys.stdout.write("\033[%d;%dH" % (y, x))
    return None


def main():
    init()
    size = shutil.get_terminal_size()
    width = size.columns // 2
    height = size.lines
    speed = 7
    speed_clone = speed
    sys.stdout.write(colors.line_home+colors.screen_clear)
    sys.stdout.write("_"*size.columns)
    snake = Snake(width, height, colors.bg.red, colors.bg.purple)
    snake.apple = Apple(size, snake, colors.bg.green)
    move_cursor((1, 1))
    sys.stdout.write(f"Speed: {speed}")
    move_cursor((10, 1))
    sys.stdout.write(f"Score: {snake.score}")
    keyboard.wait("enter")
    cursor.hide()
    while True:
        start = time.time()
        if keyboard.is_pressed("esc"):
            break
        elif keyboard.is_pressed("f5"):
            sys.stdout.write(colors.line_home+colors.screen_clear)

        if speed != speed_clone:
            speed_clone = speed
            move_cursor((1, 1))
            sys.stdout.write(f"Speed: {speed}")

        size = shutil.get_terminal_size()
        snake.move(size, (snake.apple.x, snake.apple.y), speed)

        if snake.collision():
            height = size.lines
            width = size.columns
            move_cursor((1, height // 2))
            sys.stdout.write("You lose!".center(width))
            break

        change_of_direction = False
        change_of_speed = False
        end = time.time()
        while (end - start) < (0.25 - speed / 40):
            if not change_of_direction:
                if keyboard.is_pressed("w") or keyboard.is_pressed("up arrow"):
                    if snake.direction != "down":
                        snake.direction = "up"
                        change_of_direction = True
                elif keyboard.is_pressed("a") or keyboard.is_pressed("left arrow"):
                    if snake.direction != "right":
                        snake.direction = "left"
                        change_of_direction = True
                elif keyboard.is_pressed("s") or keyboard.is_pressed("down arrow"):
                    if snake.direction != "up":
                        snake.direction = "down"
                        change_of_direction = True
                elif keyboard.is_pressed("d") or keyboard.is_pressed("right arrow"):
                    if snake.direction != "left":
                        snake.direction = "right"
                        change_of_direction = True

            if not change_of_speed:
                if keyboard.is_pressed("+"):
                    speed += 1
                    change_of_speed = True
                if keyboard.is_pressed("-"):
                    speed -= 1
                    change_of_speed = True
                if speed > 9:
                    speed = 9
                elif speed < 1:
                    speed = 1
            end = time.time()


if __name__ == "__main__":
    while True:
        main()
        time.sleep(2)
        key = keyboard.read_key()
        if key == "esc":
            break
