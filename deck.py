import characters
import weapons
import rooms
import random

class Deck(object):
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
        random.shuffle(self.cards)

    def pop(self):
        return self.cards.pop()

