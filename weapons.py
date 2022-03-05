import cards

class Weapon(cards.Card):
    """An instance of a weapon."""
    def __init__(self, name : str, imagepath : str):
        super(name, imagepath)

    def __repr__(self) -> str:
        return f"Weapon: {self.name}"