import sys
import abc

class Player(object):
    x:int
    y:int

    def __init__(self) -> None:
        self.x = 0
        self.y = 0

    def __str__(self) -> str:
        return "The player is located at ({x},{y}).".format(x=self.x, y=self.y)

class ICommand(abc.ABC):
    @abc.abstractmethod
    def execute(self, player:Player) -> None:
        pass

    @abc.abstractmethod
    def undo(self, player:Player) -> None:
        pass

class MoveDownCommand(ICommand):
    def execute(self, player: Player) -> None:
        player.y -= 1

    def undo(self, player:Player) -> None:
        player.y += 1

class MoveUpCommand(ICommand):
    def execute(self, player: Player) -> None:
        player.y += 1
    
    def undo(self, player:Player) -> None:
        player.y -= 1

class MoveLeftCommand(ICommand):
    def execute(self, player: Player) -> None:
        player.x -= 1
    
    def undo(self, player:Player) -> None:
        player.x += 1

class MoveRightCommand(ICommand):
    def execute(self, player: Player) -> None:
        player.x += 1

    def undo(self, player:Player) -> None:
        player.x -= 1

if __name__ == "__main__":
    the_player:Player = Player()
    undo_stack:list[ICommand] = []
    redo_stack:list[ICommand] = []

    while True:
        try:
            result = input("> ")

            if result == "print":
                print(the_player)
            elif result == "move up":
                command:ICommand = MoveUpCommand()
                command.execute(the_player)
                undo_stack.append(command)
            elif result == "move down":
                command:ICommand = MoveDownCommand()
                command.execute(the_player)
                undo_stack.append(command)
            elif result == "move left":
                command:ICommand = MoveLeftCommand()
                command.execute(the_player)
                undo_stack.append(command)
            elif result == "move right":
                command:ICommand = MoveRightCommand()
                command.execute(the_player)
                undo_stack.append(command)
            elif result == "undo":
                if len(undo_stack) > 0:
                    command:ICommand = undo_stack.pop()
                    command.undo(the_player)
                    redo_stack.append(command)
                else:
                    print("Nothing to undo!")
            elif result == "redo":
                if len(redo_stack) > 0:
                    command:ICommand = redo_stack.pop()
                    command.execute(the_player)
                else:
                    print("Nothing to redo!")
            else:
                print("Unrecognized input: {input}".format(input=result))

        except KeyboardInterrupt:
            sys.exit(0)