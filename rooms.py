from email.mime import image
import cards

class Room(cards.Card):
    """An instance of a room."""
    def __init__(self, name : str, imagepath : str):
        super().__init__(name, imagepath)
        self.connections = {}

    def addConnection(self, relpos : str, room : "Room"):
        self.connections[relpos] = room

    def __str__(self):
        return self.name