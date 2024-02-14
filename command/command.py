import sys
import abc
import random

class Player(object):
    x:int
    y:int

    def __init__(self) -> None:
        self.x = 0
        self.y = 0

    def __str__(self) -> str:
        return "The player is located at ({x},{y}).".format(x=self.x, y=self.y)

class GameState(object):
    the_player:Player
    the_undo_stack:list['ICommand']
    the_redo_stack:list['ICommand']

    def __init__(self) -> None:
        self.the_player = Player()
        self.the_undo_stack = []
        self.the_redo_stack = []
    
    def __str__(self) -> None:
        return str(self.the_player)

class ICommand(abc.ABC):
    @abc.abstractmethod
    def execute(self, the_game_state:GameState) -> None:
        the_game_state.the_undo_stack.append(self)

    @abc.abstractmethod
    def undo(self, the_game_state:GameState) -> None:
        the_game_state.the_redo_stack.append(self)

class MoveDownCommand(ICommand):
    def execute(self, the_game_state:GameState) -> None:
        super().execute(the_game_state)
        the_game_state.the_player.y -= 1

    def undo(self, the_game_state:GameState) -> None:
        super().undo(the_game_state)
        the_game_state.the_player.y += 1

class MoveUpCommand(ICommand):
    def execute(self, the_game_state:GameState) -> None:
        super().execute(the_game_state)
        the_game_state.the_player.y += 1
    
    def undo(self, the_game_state:GameState) -> None:
        super().undo(the_game_state)
        the_game_state.the_player.y -= 1

class MoveLeftCommand(ICommand):
    def execute(self, the_game_state:GameState) -> None:
        super().execute(the_game_state)
        the_game_state.the_player.x -= 1
    
    def undo(self, the_game_state:GameState) -> None:
        super().undo(the_game_state)
        the_game_state.the_player.x += 1

class MoveRightCommand(ICommand):
    def execute(self, the_game_state:GameState) -> None:
        super().execute(the_game_state)
        the_game_state.the_player.x += 1

    def undo(self, the_game_state:GameState) -> None:
        super().undo(the_game_state)
        the_game_state.the_player.x -= 1

class UndoCommand(ICommand):
    def execute(self, the_game_state:GameState) -> None:
        if len(the_game_state.the_undo_stack) > 0:
            command:ICommand = the_game_state.the_undo_stack.pop()
            command.undo(the_game_state)
        else:
            print("Nothing to undo!")

    def undo(self, the_game_state:GameState) -> None:
        pass

class RedoCommand(ICommand):
    def execute(self, the_game_state:GameState) -> None:
        if len(the_game_state.the_redo_stack) > 0:
            command:ICommand = the_game_state.the_redo_stack.pop()
            command.execute(the_game_state)
        else:
            print("Nothing to redo!")

    def undo(self, the_game_state:GameState) -> None:
        pass

class NoopCommand(ICommand):
    def execute(self, game_state:GameState) -> None:
        pass

    def undo(self, game_state:GameState) -> None:
        pass

class ICommandSource(abc.ABC):
    @abc.abstractmethod
    def poll(self) -> ICommand:
        pass

class UserInput(ICommandSource):
    def poll(self) -> ICommand:
        result = input("> ")

        if result == "move up":
            return MoveUpCommand()
        elif result == "move down":
            return MoveDownCommand()
        elif result == "move left":
            return MoveLeftCommand()
        elif result == "move right":
            return MoveRightCommand()
        elif result == "undo":
            return UndoCommand()
        elif result == "redo":
            return RedoCommand()
        else:
            return NoopCommand()

class RandomInput(ICommandSource):
    commands:'ShuffleBag'

    def __init__(self):
        self.commands = ShuffleBag([MoveUpCommand(), MoveDownCommand(), MoveLeftCommand(), MoveRightCommand()])

    def poll(self) -> ICommand:
        input("> ")

        return next(self.commands)

class ShuffleBag(object):
    items:list
    index:int

    def __init__(self, items:list) -> None:
        self.index = 0
        self.items = fisher_yates_shuffle(items)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.items):
            self.index = 0
            self.items = fisher_yates_shuffle(self.items)

        item = self.items[self.index]

        self.index += 1

        return item
    
def fisher_yates_shuffle(arr:list) -> list:
    for i in range(len(arr) - 1, 0, -1):
        j:int = random.randrange(0, i)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

if __name__ == "__main__":
    the_game_state:GameState = GameState()
    the_command_source:ICommandSource = UserInput()

    while True:
        try:
            the_command:ICommand = the_command_source.poll()
            the_command.execute(the_game_state)
            print(the_game_state)

        except KeyboardInterrupt:
            sys.exit(0)