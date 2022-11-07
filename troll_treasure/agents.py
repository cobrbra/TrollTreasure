""" Module containing agent classes. """

from abc import ABC, abstractmethod
import random


def direction(point_a, point_b):
    """
    Returns the direction from point_a to point_b, or None if they
    are not neighhbouring grid points.
    """
    if point_b == point_a:
        return "nowhere"
    if point_b[1] == point_a[1]:
        if point_b[0] == point_a[0] - 1:
            return "left"
        if point_b[0] == point_a[0] + 1:
            return "right"
    if point_b[0] == point_a[0]:
        if point_b[1] == point_a[1] - 1:
            return "up"
        if point_b[1] == point_a[1] + 1:
            return "down"

    return None


class Agent(ABC):
    """
    Base functionality to create and load (but not move) an Agent
    """

    def __init__(self, point, name, symbol, verbose=True, allow_wait=True, **__):
        self.point = tuple(point)  # (x, y) grid location of the agent
        self.name = name  # e.g. adventurer or troll
        self.symbol = symbol  # single char symbol to show the agent on dungeon maps
        self.verbose = verbose  # print output on agent behaviour if True
        self.allow_wait = allow_wait  # allow the agent to move nowhere

    @abstractmethod
    def move(self, rooms):
        """Method specifying rules for movement of agent."""

    @classmethod
    def from_dict(cls, agent_dict):
        """Allows the creation of agent from dictionary."""
        return cls(
            agent_dict["point"],
            agent_dict["name"],
            agent_dict["symbol"],
            allow_wait=agent_dict["allow_wait"],
        )


class RandomAgent(Agent):
    """
    Agent that makes random moves
    """

    def move(self, rooms):
        if not rooms[self.point].links:
            # this room isn't linked to anything, can't move
            if self.verbose:
                print(f"{self.name} is trapped")
            return

        # pick a random room to move to
        options = rooms[self.point].links
        if self.allow_wait:
            options.append(self)
        new_room = random.choice(options)

        if self.verbose:
            move = direction(self.point, new_room.point)
            print(f"{self.name} moves {move}")
        self.point = new_room.point


class HumanAgent(Agent):
    """
    Agent that prompts the user where to move next
    """

    def move(self, rooms):
        if not rooms:
            if self.verbose:
                print(f"{self.name} is trapped")
            return
        # populate movement options depending on available rooms
        if self.allow_wait:
            options = ["wait"]
        else:
            options = []
        if (self.point[0] - 1, self.point[1]) in rooms:
            options.append("left")
        if (self.point[0] + 1, self.point[1]) in rooms:
            options.append("right")
        if (self.point[0], self.point[1] - 1) in rooms:
            options.append("up")
        if (self.point[0], self.point[1] + 1) in rooms:
            options.append("down")

        # prompt user for movement input
        choice = None
        while choice not in options:
            choice = input(f"Where will {self.name} move \n{options}? ")

        # move the agent
        if choice == "left":
            self.point = (self.point[0] - 1, self.point[1])
        elif choice == "right":
            self.point = (self.point[0] + 1, self.point[1])
        elif choice == "up":
            self.point = (self.point[0], self.point[1] - 1)
        elif choice == "down":
            self.point = (self.point[0], self.point[1] + 1)
