import cards

class Character(cards.Card):
    """Represents an in-game character (not an actual player)."""
    def __init__(self, name : str, imagepath : str, hexcolour : str):
        super(name, imagepath)
        self.colour = hexcolour

    def getColour(self):
        return self.colour