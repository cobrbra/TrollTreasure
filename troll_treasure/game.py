""" Module containing main Game class for troll treasure game."""

from argparse import ArgumentParser
import copy

from art import tprint

from .dungeon import Dungeon


class Game:
    """Run a troll dungeon game."""

    def __init__(self, dungeon):
        self.dungeon = dungeon

    def preamble(self):
        """Print opening text for dungeon game."""
        tprint("Troll Treasure\n", font="small")
        print(
            f"""
The {self.dungeon.adventurer.name} is looking for treasure in a mysterious dungeon.
Will they succeed or be dinner for the {self.dungeon.troll.name} that lurks there?

The map of the dungeon is below:
o : an empty room
o - o : connected rooms
{self.dungeon.troll.symbol} : {self.dungeon.troll.name}
{self.dungeon.adventurer.symbol} : {self.dungeon.adventurer.name}
{self.dungeon.treasure.symbol} : the treasure
            """
        )

    def run(self, max_steps=1000, verbose=True, start_prompt=False):
        """Run game!"""
        dungeon = copy.deepcopy(self.dungeon)
        dungeon.set_verbose(verbose)
        if verbose:
            self.preamble()
            dungeon.draw()
            if start_prompt:
                input("\nPress enter to continue...")
            else:
                print("\nLet the hunt begin!")

        result = 0
        for turn in range(max_steps):
            result = dungeon.outcome()
            if verbose:
                if result == 1:
                    print(f"\n{self.dungeon.adventurer.name} gets the treasure and returns a hero!")
                    tprint("WINNER", font="small")
                    return result
                elif result == -1:
                    print(f"\n{self.dungeon.troll.name} will eat tonight!")
                    tprint("GAME OVER", font="small")
                    return result
                else:
                    print(f"\nTurn {turn + 1}")

            dungeon.update()

        # no outcome in max steps (e.g. no treasure and troll can't reach adventurer)
        if verbose:
            print(
                f"\nNo one saw {self.dungeon.adventurer.name} or {self.dungeon.troll.name} again."
            )
            tprint("STALEMATE", font="small")

        return result

    def probability(self, trials=10000, max_steps=1000, verbose=False):
        """Calculate probability of different outcomes for random game."""
        outcomes = {-1: 0.0, 0: 0.0, 1: 0.0}
        for _ in range(trials):
            result = self.run(max_steps=max_steps, verbose=verbose)
            try:
                outcomes[result] += 1
            finally:
                pass
        for result in outcomes:
            outcomes[result] = outcomes[result] / trials
        return outcomes


def play():
    """Play Troll Treasure (accessible from the command line)."""
    parser = ArgumentParser(description="Supply details for Troll Treasure game.")
    parser.add_argument("--dungeon_file", "-d")
    parser.add_argument("--probabilities", "-p", action="store_true")

    args = parser.parse_args()

    game_dungeon = Dungeon.from_file(args.dungeon_file)
    game = Game(game_dungeon)
    if args.probabilities:
        game.probability(max_steps=10)
    else:
        game.run()


if __name__ == "__main__":
    play()
