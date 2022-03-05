import cards

class Room(cards.Card):
    """An instance of a room."""
    def __init__(self, name : str, imagepath : str):
        super(name, imagepath)
        self.connections = {}

    def addConnection(self, relpos : str, room : "Room"):
        self.connections[relpos] = room