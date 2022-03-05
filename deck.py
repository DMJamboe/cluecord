import characters
import weapons
import rooms
import random

class Deck(Object):
    """The deck of cards"""
    def __init__(self, characterList : "list[characters.Character]" , weaponList : "list[weapons.Weapon]", roomList : "list[rooms.Room]"):
        self.cards = []
        #add characters
        for character in characterList:
            self.cards.append(character)
        #add weapons
        for weapon in weaponList:
            self.cards.append(weapon)
        #add rooms
        for room in roomList:
            self.cards.append(room)

    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.cards)

    def pop(self):
        """Return the first card from the deck (removing it from the deck)"""
        return self.cards.pop()

