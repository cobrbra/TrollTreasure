""" Module containing classes and helper functions for specifying dungeon grid layout. """

import yaml

from .agents import RandomAgent, HumanAgent
from .rooms import Rooms


class Treasure:
    """Specifies treasure object consisting of a location and symbol."""

    def __init__(self, point, symbol):
        self.point = tuple(point)  # (x, y) grid location of the treasure
        self.symbol = symbol  # single char symbol to show the treasure on dungeon maps

    @classmethod
    def from_dict(cls, treasure_dict):
        """Allows creation of treasure object from dictionary."""
        return cls(treasure_dict["point"], treasure_dict["symbol"])


class Dungeon:
    """
    Dungeon with:
    - Connected set of rooms on a square grid
    - The location of some treasure
    - An adventurer agent with an initial position
    - A troll agent with an initial position
    """

    def __init__(self, rooms, treasure, adventurer, troll, verbose=True):
        self.rooms = rooms
        self.treasure = treasure
        self.adventurer = adventurer
        self.troll = troll
        self.verbose = verbose

        # the extent of the square grid
        self.xlim = (
            min(r.point[0] for r in self.rooms),
            max(r.point[0] for r in self.rooms),
        )
        self.ylim = (
            min(r.point[1] for r in self.rooms),
            max(r.point[1] for r in self.rooms),
        )

        self._validate()

    def _validate(self):
        if self.treasure.point not in self.rooms:
            raise ValueError(f"Treasure{self.treasure.point} is not in the dungeon")
        if self.adventurer.point not in self.rooms:
            raise ValueError(f"{self.adventurer.name}{self.treasure.point} is not in the dungeon")
        if self.troll.point not in self.rooms:
            raise ValueError(f"{self.troll.name}{self.treasure.point} is not in the dungeon")

    @classmethod
    def from_file(cls, path):
        """Allow creation of dungeon object from configuration file."""
        with open(path, encoding="utf-8") as dungeon_file:
            spec = yaml.safe_load(dungeon_file)
        rooms = Rooms.from_list(spec["rooms"])
        treasure = Treasure.from_dict(spec["treasure"])

        agent_keys = ["adventurer", "troll"]
        agents = {}
        for agent in agent_keys:
            if spec[agent]["type"] == "random":
                agent_class = RandomAgent
            elif spec[agent]["type"] == "human":
                agent_class = HumanAgent
            else:
                raise ValueError(f"Unknown agent type {spec[agent]['type']}")
            agents[agent] = agent_class(**spec[agent])

        return cls(rooms, treasure, agents["adventurer"], agents["troll"])

    def update(self):
        """
        Move the adventurer and the troll
        """
        self.adventurer.move(self.rooms)
        self.troll.move(self.rooms)
        if self.verbose:
            print()
            self.draw()

    def outcome(self):
        """
        Check whether the adventurer found the treasure or the troll
        found the adventurer
        """
        if self.adventurer.point == self.troll.point:
            return -1
        if self.adventurer.point == self.treasure.point:
            return 1
        return 0

    def set_verbose(self, verbose):
        """Set whether to print output"""
        self.verbose = verbose
        self.adventurer.verbose = verbose
        self.troll.verbose = verbose

    def draw(self):
        """Draw a map of the dungeon"""
        layout = ""

        for y_coord in range(self.ylim[0], self.ylim[1] + 1):
            for x_coord in range(self.xlim[0], self.xlim[1] + 1):
                # room and character symbols
                if (x_coord, y_coord) in self.rooms:
                    if self.troll.point == (x_coord, y_coord):
                        layout += self.troll.symbol
                    elif self.adventurer.point == (x_coord, y_coord):
                        layout += self.adventurer.symbol
                    elif self.treasure.point == (x_coord, y_coord):
                        layout += self.treasure.symbol
                    else:
                        layout += "o"
                else:
                    layout += " "

                # horizontal connections
                if ((x_coord, y_coord) in self.rooms) and (
                    ((x_coord + 1), y_coord) in self.rooms[(x_coord, y_coord)]
                ):
                    layout += " - "
                else:
                    layout += "   "

            # vertical connections
            if y_coord < self.ylim[1]:
                layout += "\n"
                for x_coord in range(self.xlim[0], self.xlim[1] + 1):
                    if ((x_coord, y_coord) in self.rooms) and (
                        (x_coord, y_coord + 1) in self.rooms[(x_coord, y_coord)]
                    ):
                        layout += "|"
                    else:
                        layout += " "
                    if x_coord < self.xlim[1]:
                        layout += "   "
                layout += "\n"

        print(layout)
