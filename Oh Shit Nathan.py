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
        self.photo = ImageTk.PhotoImage(Image.open(name + " " + self.suit + ".jpg"))

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

    def guess(self):
        return self.guess

    def name(self):
        return self.name

    def cards(self):
        return self.cards

class HumanPlayer(Player):
    def dealCards(self, cards):
        self.cards = cards

    def guessWin(self, guess):
        self.guess = guess

def checkNumPlayers(*args):
    global numPlayInt
    try:
        numPlayStr = numPlayers.get()
        numPlayInt = int(numPlayStr)
        afterFirstScreen()
    except(ValueError):
        pass

def afterFirstScreen(*args):
    # Set Enter key to appropriate new command
    root.bind('<Return>', getPlayerNames)
    # Put cursor into textbox for entry
    nameEntry.focus()
    # Destroy the first screen
    frame1.destroy()
    # Put frame2 on the grid to display it
    frame2.grid(row = 0, column = 0)

def getPlayerNames(*args):
    if getName.get() != '':
        global counterGetName
        playerNames.append(getName.get())
        if counterGetName == int(numPlayers.get())-1:
            root.bind('<Return>', afterSecondScreen)
            Enter2["command"] = afterSecondScreen
        #clear the entry box
        nameEntry.delete(0, "end")
        counterGetName += 1
        nameLabel.configure(text=f"What's your name, player {counterGetName}?")

def makePlayers(*args):
    for name in playerNames:
        players.append(HumanPlayer(name))

def afterSecondScreen(*args):
    # Add Last Name
    playerNames.append(getName.get())
    # Put cursor into textbox for entry
    winEntry.focus()
    # Create players with player names
    makePlayers()
    # Set up who is going to be first at the start of the game
    curPlayer = random.randint(0,len(players)-1)
    # Destroy the second screen
    frame2.destroy()
    # Grid frame 3 so that it displays
    frame3.grid(row = 0, column = 0)
    # Set current player to player 1
    outerGameLoop()

def makeCards(*args):
    global deck
    deck = []
    for c in range(52):
        deck.append(Card(c))

def dealCards(*args):
    for c in range(roundNum):
        for i in range(len(players)):
            randnum = random.randint(0, len(deck)-1)
            Player.addCard(players[i], deck[randnum])
            deck.pop(randnum)
    randnum = random.randint(0, len(deck)-1)
    global trumpCard
    trumpCard = deck[randnum]
    deck.pop(randnum)

def deletePrevGuesses(*args):
    for c in range(len(prevGuesses)-1, -1, -1):
        prevGuesses[c].destroy
        prevGuesses.pop(c)

def outerGameLoop(*args):
    # Make new deck
    makeCards()
    # Deal Cards
    dealCards()
    # Change trump card image
    trumpCardImage["image"] = trumpCard.photoImage()
    # Set counter3 to 0
    global counter3
    counter3 = 0
    # Delete previous guesses
    deletePrevGuesses()
    # Set up what round it is
    roundNumLabel["text"] = "There are " + str(roundNum) + " cards this round"
    # Go to pass to screen
    passTo()

def deleteDisplayedCards(*args):
    for c in range(len(cardDisplay)-1, -1, -1):
        cardDisplay[c].destroy()
        cardDisplay.pop(c)

def displayCards(*args):
    c = 0
    for card in Player.cards(players[curPlayer]):
        cardDisplay.append(ttk.Label(frame3, image = card.photoImage()))
        cardDisplay[c].grid(row = 2, column = c+1, sticky = (N, E, W, S), padx = 5, pady = 5)
        c += 1

def nextPlayer(*args):
    global curPlayer
    curPlayer += 1
    if curPlayer == len(players):
        curPlayer = 0

def getNumWins(*args):
    global counter3
    global curPlayer
    # Put cursor in entrybox
    winEntry.focus()
    # Stop displaying frame 4
    frame4.grid_remove()
    # Display frame 3
    frame3.grid(row = 0, column = 0)
    # Set text for asking for the players guess to say the name
    winLabel["text"] = "How many cards will you win, " + Player.name(players[curPlayer]) + "? "
    # Destroy previously displayed cards
    deleteDisplayedCards()
    # Display all cards
    displayCards()
    try:
        # Convert value in entry box to an integer
        winsInt = int(getWins.get())
        Player.guessWin(players[curPlayer], winsInt)
        # display what previous people have guessed they will win
        # Create a new widget to dislay what previous players guessed, and add to the list
        name = Player.name(players[curPlayer])
        prevGuesses.append(ttk.Label(frame3, text = f"Player {name} guessed: " + getWins.get()))
        prevGuesses[counter3].grid(row = 0, column = 2 + counter3, sticky = (N, W, E, S), padx = 5, pady = 5)
        # Increment counter
        counter3 += 1
        # Increment to next player
        nextPlayer()
        # Clear the entry box
        winEntry.delete(0, "end")
        if counter3 == int(numPlayers.get()):
            innerGameLoop()
        # Bring us to pass to screen
        passTo()
    except(ValueError):
        pass

def passTo(*args):
    # Stop displaying frame 3
    frame3.grid_remove()
    # Display frame 4
    frame4.grid(row = 0, column = 0)
    # Set name of player in appropriate widgets
    playerPass["text"] = "Pass to " + Player.name(players[curPlayer])
    confirmPlayer["text"] = "I am " + Player.name(players[curPlayer])
    # Set Enter key to command for after pass
    root.bind('<Return>', getNumWins)
    # Set button command for after pass
    confirmPlayer["command"] = getNumWins

def innerGameLoop(*args):
    frame3.destroy()
    frame4.destroy()

# Create a root window to show to the screen and title it Oh Shit
root = Tk()
root.title("Oh Shit")

# Variables:
# List of players and their names, to be filled in getNames
playerNames = []
# List of players and their wins, to be filled in getWins
wins = []
# Create a variable to hold the number of players
numPlayers = StringVar()
# Create a variable to hold the integer version of number of players
numPlayInt = 0
# Create a variable to hold the name of players
getName = StringVar()
# Create a variable to hold the number of wins
getWins = StringVar()
# Create a list to hold player objects
players = []
# Create an int variable to hold round number the game is on
roundNum = 10
# Create a list to hold cards for the deck
deck = []
# Create a counter for getting names
counterGetName = 1
# Variable to hold current player
curPlayer = 0
# Variable to hold trump card
trumpCard = Card(0)
# List to hold the card widgets that are used in frame 3
cardDisplay = []
# Counter for frame 3
counter3 = 0
# Create a list for previous players guesses
prevGuesses = []

# Frame1: Get number of players
frame1 = ttk.Frame(root, padding = "3 3 12 12")
frame1.grid(column=0, row=0, sticky=(N, W, E, S))
# Label for number of players
numlabel = ttk.Label(frame1, text = "Number of Players: ")
numlabel.grid(row = 0, column = 0)
# Number of players entry box
numEntry = ttk.Entry(frame1, textvariable = numPlayers)
numEntry.grid(row=0, column=1)
# Create an "Enter!" button and go to the next screen
Enter = ttk.Button(frame1, text = "Enter!", command = checkNumPlayers) 
Enter.grid(row=1, column=1)
# Create spacing around each widget
for child in frame1.winfo_children(): child.grid_configure(padx=5, pady=5, sticky = (N, W, E, S))
# State with the cursor in the textbot
numEntry.focus()
# Bind return to also bring us to the next screen
root.bind('<Return>', checkNumPlayers)

# Frame2: Get names of players
frame2 = ttk.Frame(root, padding = "3 3 12 12")
# Create text on the screen to ask what the player's name is
nameLabel = ttk.Label(frame2, text = "What's your name, player 1?")
nameLabel.grid(row = 0, column = 0)
# Create an entry box for players to input their name
nameEntry = ttk.Entry(frame2, textvariable = getName)
nameEntry.grid(row=0, column=1)
# Create an "Enter!" button and go to the next screen
Enter2 = ttk.Button(frame2, text = "Enter!", command = getPlayerNames) 
Enter2.grid(row=1, column=1)
# Spacing around each widget
for child in frame2.winfo_children(): child.grid_configure(padx=5, pady=5, sticky = (N, W, E, S))

# Frame3: Get the number of wins for the round
frame3 = ttk.Frame(root, padding = "3 3 12 12")
# Create the widgets for screen 3:
# Label to ask how many cards a player will win
winLabel = ttk.Label(frame3, text = "How many cards will you win? ")
winLabel.grid(row = 0, column = 0)
# Create an entry box for players to input how many cards they wilil win
winEntry = ttk.Entry(frame3, textvariable = getWins)
winEntry.grid(row=0, column=1)
# Create an "Enter!" button and go to the next screen
Enter3 = ttk.Button(frame3, text = "Enter!", command = getNumWins) 
Enter3.grid(row=1, column=1, sticky = (N, W, E, S))
# Create label to say what round we are on
roundNumLabel = ttk.Label(frame3)
roundNumLabel.grid(row = 1, column = 0)
# Create label to say what the player's cards are
playerCardLabel = ttk.Label(frame3, text = "Your cards:")
playerCardLabel.grid(row = 2, column = 0)
# Create label for trump card
trumpCardLabel = ttk.Label(frame3, text = "Trump card:")
trumpCardLabel.grid(row = 1, column = 2)
# Create label for trump card image
trumpCardImage = ttk.Label(frame3)
trumpCardImage.grid(row = 1, column = 3)
# Spacing around each widget
for child in frame3.winfo_children(): child.grid_configure(padx=5, pady=5, sticky = (N, W, E, S))

# Frame4: pass to screen
frame4 = ttk.Frame(root, padding = "3 3 12 12")
# Create the widgets for screen 4:
# Create Label to say who to pass to
playerPass = ttk.Label(frame4)
playerPass.grid(row = 0, column = 0)
# Create button to press
confirmPlayer = ttk.Button(frame4)
confirmPlayer.grid(row = 0, column = 1)
for child in frame4.winfo_children(): child.grid_configure(padx=5, pady=5, sticky = (N, W, E, S))
