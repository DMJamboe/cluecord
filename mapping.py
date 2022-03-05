from rooms import Room
from player import Player
from discord import TextChannel
from PIL import Image, ImageDraw

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

        library.addConnection("Library", library)
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

        self.rooms = [billiardRoom, foyer, library, hall, diningRoom, kitchen, lounge, ballroom, conservatory]

        self.roomCoords = {"Billiard Room" : (407, 272)}

    def __str__(self):
        result = ""
        for room in self.rooms:
            result += "\n" + str(room)
        return result

    def createMapImage(self, players : "list[Player]", id : TextChannel):
        """Creates an image of the current board state, naming the file the id of the text channel currently playing the game"""
        with Image.open("Board.png") as board:
            draw = ImageDraw.Draw(board)
            draw.regular_polygon(self.roomCoords["Billiard Room"], 1, rotation=0, fill="red", outline=None)



        
