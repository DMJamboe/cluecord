class Card(object):
    """An object representing an abstract card."""
    def __init__(self, name: str, imagepath: str):
        self.name : str = name
        self.imagepath : str = imagepath

    def __repr__(self):
        return f"Card of {self.name}"

    def getName(self):
        return self.name

    def getImagePath(self):
        return self.imagepath
