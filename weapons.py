import cards

class Weapon(cards.Card):
    """An instance of a weapon."""
    def __init__(self, name : str, imagepath : str):
        super().__init__(name, imagepath)

    def __repr__(self) -> str:
        return f"Weapon: {self.name}"