"""" Module containing classes for rooms in troll game. """

from .agents import direction


class Room:
    """Class for room objects in troll game."""

    def __init__(self, point, links=None):
        self.point = tuple(point)  # grid point of this room
        self.links = links  # other rooms this rooms connects to
        self._validate_links()

    def __contains__(self, point):
        """
        `(x, y) in room_instance` returns `True` if `room_instance` has a link to
        a room at point `(x, y)`
        """
        if self.links is not None:
            return point in [link.point for link in self.links]
        return False

    def _validate_links(self):
        """
        Verifies all linked rooms are at neighbouring grid points
        """
        if not self.links:
            return
        for link in self.links:
            if not direction(self.point, link.point):
                raise ValueError(f"Invalid link: {link.point} is not connected to {self.point}")


class Rooms:
    """
    Collection of rooms
    """

    def __init__(self, rooms):
        # rooms dictionary keyed by (x, y) coordinate (grid cell indices)
        self.rooms = {r.point: r for r in rooms}

    def __iter__(self):
        """
        Allows Rooms objects to be iterated over (see Module 7)
        """
        return iter(self.rooms.values())

    def __getitem__(self, point):
        """
        rooms[(x, y)] will retrieve the room at coordinate (x, y) (where
        rooms is an instance of the Rooms class)
        """
        return self.rooms[point]

    def __contains__(self, point):
        """
        (x, y) in rooms will return True if a room at coordinates (x, y)
        is in rooms (where rooms is an instance of the Rooms class)
        """
        return point in self.rooms

    @classmethod
    def from_list(cls, room_list):
        """Allows the construction of a Rooms object from a list of dictionaries."""
        rooms = [Room(room["point"], [Room(link) for link in room["links"]]) for room in room_list]
        return cls(rooms)
