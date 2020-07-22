from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import random

# class for Cards
class Card():
    #Initialize itself with a value and a photoimage
    def __init__(self, num):
        self.value = num%13
        if self.value < 9:
            name = str(self.value + 2)
        elif self.value == 9:
            name = "Jack"
        elif self.value == 10:
            name = "Queen"
        elif self.value == 11:
            name = "King"
        else:
            name = "Ace"
        if num < 13:
            self.suit = "Hearts"
        elif num < 26:
            self.suit = "Diamonds"
        elif num < 39:
            self.suit = "Clubs"
        else:
            self.suit = "Spades"
        self.photo = ImageTk.PhotoImage(Image.open(name + " " + suit + ".jpg"))

    def photoImage(self):
        return self.photo

    def value(self):
        return self.value

    def suit(self):
        return self.suit

class Player():
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.point = 0
        self.guess = 0

    def addCard(self, card):
        self.cards.append(card)

    def removeCard(self, i):
        self.cards.pop(i)

    def guessWin(self, guess):
        pass

class HumanPlayer(Player):
    def dealCards(self, cards):
        self.cards = cards

    def guessWin(self, guess):
        self.guess = guess

def makePlayers(*args):
    for name in playerNames:
        players.append(HumanPlayer(name))

def makeCards(*args):
    for c in range(len(deck)-1, -1, -1):
        deck.pop(c)
    tmpCards = []
    for c in range(52):
        tmpCards.append(Card(c))

def dealCards(*args):
    for c in range(roundNum):
        for i in range(len(players)):
            randnum = random.randint(0, len(deck)-1)
            Player.addCard(players[i], deck[randnum])
            deck.pop(randnum)
        
        

# Create a root windown to show to the screen and title it War
root = Tk()
root.title("War")
playerNames = ["Paul", "Stephanie", "Helen"]
players = []
roundNum = 10
deck = []
# Create a frame
frame1 = ttk.Frame(root, padding = "3 3 12 12")
frame1.grid(column=0, row=0, sticky=(N, W, E, S))
# Create a second frame
frame2 = ttk.Frame(root, padding = "3 3 12 12")
frame2.grid(column=0, row=0, sticky=(N, W, E, S))
# Lower this second frame below the first frame
frame2.lower(frame1)


root.mainloop()
