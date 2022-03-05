from rooms import Room
from player import Player
from discord import TextChannel
from PIL import Image, ImageDraw
import sys
import operator

class Map(object):
    """The game map."""


    def __init__(self, imagepath: str):
        self.imagepath = imagepath
        # Creates all rooms and connections
        billiardRoom = Room("Billiard Room", "https://upload.wikimedia.org/wikipedia/commons/5/5d/Franz_Heinrich_001.jpg")
        foyer = Room("Foyer", "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/19talbot-cooley-portfolio-interiors-gallery-foyer-architectural-detail-1578500748.jpg")
        library = Room("Library", "https://cdn.britannica.com/92/216092-050-4B31C2B7/custom-library.jpg?q=60")
        lounge = Room("Lounge", "https://media-cdn.tripadvisor.com/media/photo-s/10/39/32/c7/akun-lounge-and-bar.jpg")
        hall = Room("Hall", "https://roomdsign.com/wp-content/uploads/2020/06/how-to-lighten-a-dark-narrow-hallway.jpg")
        diningRoom = Room("Dining Room", "https://static.wikia.nocookie.net/freddy-fazbears-pizza/images/5/58/DiningAreaNoCamera.png/revision/latest?cb=20140825033602")
        kitchen = Room("Kitchen", "https://harewood.org/wp-content/uploads/2014/03/Old-Kitchen-angled-1024x682.jpg")
        ballroom = Room("Ballroom" , "https://static.wikia.nocookie.net/dumbledoresarmyroleplay/images/9/9e/EdinburghBallroom.jpg/revision/latest?cb=20181207051150")
        conservatory = Room("Conservatory", "https://i.pinimg.com/originals/ea/54/40/ea5440f19515177df2274df72465b79c.jpg")

        # Pls ignore how ugly and bad this code is -- all that matters is it works :)
        billiardRoom.addConnection("Foyer", foyer)
        billiardRoom.addConnection("Lounge", lounge)
        billiardRoom.addConnection("Secret Passage", kitchen)
        
        foyer.addConnection("Billiard Room", billiardRoom)
        foyer.addConnection("Library", library)
        foyer.addConnection("Hall", hall)

        library.addConnection("Foyer", foyer)
        library.addConnection("Secret Passage", conservatory)

        hall.addConnection("Foyer", foyer)
        hall.addConnection("Dining Room", diningRoom)
        hall.addConnection("Lounge", lounge)
        hall.addConnection("Ballroom", ballroom)

        diningRoom.addConnection("Hall", hall)
        diningRoom.addConnection("Kitchen", kitchen)

        kitchen.addConnection("Dining Room", diningRoom)
        kitchen.addConnection("Secret Passage", billiardRoom)

        lounge.addConnection("Billard Room", billiardRoom)
        lounge.addConnection("Hall", hall)

        ballroom.addConnection("Hall", hall)
        ballroom.addConnection("Conservatory", conservatory)

        conservatory.addConnection("Ballroom", ballroom)
        conservatory.addConnection("Secret Passage", library)

        self.rooms = [hall, billiardRoom, foyer, library, diningRoom, kitchen, lounge, ballroom, conservatory]

        self.roomCoords = {"Billiard Room" : (457, 360), 
                           "Hall" : (1550, 930), 
                           "Foyer" : (1550, 380), 
                           "Library" : (2540, 330), 
                           "Dining Room" : (2500, 1030), 
                           "Kitchen" : (2740, 1630), 
                           "Conservatory" : (2460, 2200),
                           "Ballroom": (1550, 1870),
                           "Lounge" : (420, 1460)}

        # Contains the offsets from the center of each room to different points to show the players
        self.offsets = {0 : (-90, -40),
                        1 : (0, -40), 
                        2: (90, -40), 
                        3: (-90, 40), 
                        4: (0, 40), 
                        5 : (90, 40)} 

    def __str__(self):
        result = ""
        for room in self.rooms:
            result += "\n" + str(room)
        return result

    def createMapImage(self, players : "list[Player]", id : str):
        roomCounts = {"Billiard Room" : 0, 
                      "Hall" : 0, 
                      "Foyer" : 0, 
                      "Library" : 0, 
                      "Dining Room" : 0, 
                      "Kitchen" : 0, 
                      "Conservatory" : 0,
                      "Ballroom": 0,
                      "Lounge" : 0}
        with Image.open("Board.jpg") as board:
            draw = ImageDraw.Draw(board)
            for player in players:
                count = roomCounts[player.getRoom().name]
                draw.regular_polygon((tuple(map(operator.add, self.roomCoords[player.getRoom().name], self.offsets[count])), 40), 6, rotation=0, fill=player.character.getColour(), outline="black")
                roomCounts[player.getRoom().name] += 1
            board.save(str(id) + ".jpg")
            print("done")

    def testImage(self):
        """Creates an image of the current board state, naming the file the id of the text channel currently playing the game"""
        with Image.open("Board.png") as board:
            draw = ImageDraw.Draw(board)
            #draw.regular_polygon((self.roomCoords["Billiard Room"], 50), 4, rotation=0, fill="green", outline=None)
            draw.regular_polygon((tuple(map(operator.add, self.roomCoords["Lounge"], self.offsets[0])), 40), 6, rotation=0, fill="red", outline=None)
            draw.regular_polygon((tuple(map(operator.add, self.roomCoords["Lounge"], self.offsets[1])), 40), 6, rotation=0, fill="green", outline=None)
            draw.regular_polygon((tuple(map(operator.add, self.roomCoords["Lounge"], self.offsets[2])), 40), 6, rotation=0, fill="blue", outline=None)
            draw.regular_polygon((tuple(map(operator.add, self.roomCoords["Lounge"], self.offsets[3])), 40), 6, rotation=0, fill="white", outline="black")
            draw.regular_polygon((tuple(map(operator.add, self.roomCoords["Lounge"], self.offsets[4])), 40), 6, rotation=0, fill="yellow", outline=None)
            draw.regular_polygon((tuple(map(operator.add, self.roomCoords["Lounge"], self.offsets[5])), 40), 6, rotation=0, fill="purple", outline=None)
            board.save("123.png")

    def getStartingRoom(self):
        print (self.rooms[0])
        return self.rooms[0]


        
