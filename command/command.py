import sys

class Player(object):
    x:int
    y:int

    def __init__(self) -> None:
        self.x = 0
        self.y = 0

    def __str__(self) -> str:
        return "The player is located at ({x},{y}).".format(x=self.x, y=self.y)

    def move_up(self) -> None:
        self.y += 1

    def move_down(self) -> None:
        self.y -= 1

    def move_left(self) -> None:
        self.x -= 1
    
    def move_right(self) -> None:
        self.x += 1

if __name__ == "__main__":
    the_player = Player()

    while True:
        try:
            result = input("> ")

            if result == "print":
                print(the_player)
            elif result == "move up":
                the_player.move_up()
            elif result == "move down":
                the_player.move_down()
            elif result == "move left":
                the_player.move_left()
            elif result == "move right":
                the_player.move_right()
            elif result == "undo":
                pass
            elif result == "redo":
                pass

        except KeyboardInterrupt:
            sys.exit(0)