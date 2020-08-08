from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import random

# class for Cards
class Card():
    #Initialize itself with a value and a photoimage
    def __init__(self, num):
        self.value = num%13
        self.suit = num%4
        suits = ["Diamonds", "Clubs", "Hearts", "Spades"]
        nums = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        img = Image.open(nums[self.value] + " " + suits[self.suit] + ".jpg")
        self.image = ImageTk.PhotoImage(img.resize((round(img.size[0] * .7), round(img.size[1] * .7))))
        
    def photoImage(self):
        return self.image

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
        self.score = 0
        self.picked = Card(0)
        self.pickedCard = False
        self.wins = 0

    def addCard(self, card):
        self.cards.append(card)

    def removeCard(self, i):
        self.cards.pop(i)

    def guessWin(self, guess):
        pass

    def numWins(self, wins):
        pass

    def pickCard(self, picked):
        pass

    def guess(self):
        return self.guess

    def name(self):
        return self.name

    def cards(self):
        return self.cards

    def score(self):
        return self.score

    def picked(self):
        return self.picked

    def hasPicked(self):
        return self.pickedCard

    def resetPickedCard(self):
        self.pickedCard = False

    def wins(self):
        return self.wins

    def addScore(self, points):
        self.score += points

    def addWin(self):
        self.wins += 1

    def resetWin(self):
        self.wins = 0

    def sortCardsHighFirst(self, trump):
        for c in range(len(self.cards)-1):
            maximum = c
            for i in range(c+1, len(self.cards)):
                if Card.suit(self.cards[i]) == Card.suit(trump):
                    if Card.suit(self.cards[maximum]) == Card.suit(trump):
                        if Card.value(self.cards[i]) > Card.value(self.cards[maximum]):
                            maximum = i
                    else:
                        maximum = i
                elif Card.suit(self.cards[maximum]) != Card.suit(trump):
                    if Card.suit(self.cards[i]) > Card.suit(self.cards[maximum]):
                        maximum = i
                    elif Card.suit(self.cards[i]) == Card.suit(self.cards[maximum]) and Card.value(self.cards[i]) > Card.value(self.cards[maximum]):
                        maximum = i
            self.cards[maximum], self.cards[c] = self.cards[c], self.cards[maximum]

class HumanPlayer(Player):
    def dealCards(self, cards):
        self.cards = cards

    def guessWin(self, guess):
        self.guess = guess

    def pickCard(self, card):
        self.picked = card
        self.pickedCard = True

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
        if counterGetName == int(numPlayers.get()):
            afterSecondScreen()
        else:
            #clear the entry box
            nameEntry.delete(0, "end")
            counterGetName += 1
            nameLabel.configure(text=f"What's your name, player {counterGetName}?")

def makePlayers(*args):
    for name in playerNames:
        players.append(HumanPlayer(name))

def afterSecondScreen(*args):
    # Put cursor into textbox for entry
    winEntry.focus()
    # Create players with player names
    makePlayers()
    # Set round number
    global roundNum
    roundNum = int(52/len(players))
    if 52%len(players) == 0:
        roundNum -= 1
    global prevStartPlayer
    # Set up who is going to be first at the start of the game
    prevStartPlayer = random.randint(0,len(players)-1)
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

def sortCards(trumpCard):
    for player in players:
        Player.sortCardsHighFirst(player, trumpCard)

def deletePrevGuesses(*args):
    for c in range(len(prevGuesses)-1, -1, -1):
        prevGuesses[c].destroy()
        prevGuesses.pop(c)

def showScore():
    for i in range(len(guessScoreList)-1, -1, -1):
        guessScoreList[i].destroy()
        guessScoreList.pop(i)
    for i in range(len(players)):
        guessScoreList.append(ttk.Label(frame3, text = f"{Player.name(players[i])}'s score: {Player.score(players[i])}"))
        guessScoreList[i].grid(row = 1, column = 3+i, padx = 5, pady = 5)

def outerGameLoop(*args):
    # Make new deck
    makeCards()
    # Deal Cards
    dealCards()
    # Sort Cards
    sortCards(trumpCard)
    # Set person to start this round
    global curPlayer
    global prevStartPlayer
    curPlayer = prevStartPlayer
    nextPlayer()
    prevStartPlayer = curPlayer
    # Change trump card image
    trumpCardImage["image"] = trumpCard.photoImage()
    # Set counter3 to 0
    global counter3
    counter3 = 0
    showScore()
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
        cardDisplay[c].grid(row = 3, column = c+1, padx = 5, pady = 5)
        c += 1

def nextPlayer(*args):
    global curPlayer
    curPlayer += 1
    if curPlayer == len(players):
        curPlayer = 0

def getNumWins(*args):
    global counter3
    global curPlayer
    global players
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
        HumanPlayer.guessWin(players[curPlayer], winsInt)
        # Create a new widget to dislay what previous players guessed, and add to the list
        name = Player.name(players[curPlayer])
        prevGuesses.append(ttk.Label(frame3, text = f"Player {name} guessed: " + getWins.get()))
        prevGuesses[counter3].grid(row = 0, column = 3 + counter3, padx = 5, pady = 5)
        # Increment counter
        counter3 += 1
        # Increment to next player
        nextPlayer()
        # Clear the entry box
        winEntry.delete(0, "end")
        if counter3 == len(players):
            afterGetWins()
        # Bring us to pass to screen
        else:
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

# Display the trump card
def DisplayTrump():
    global trumpCard
    trumpImage5["image"] = trumpCard.photoImage()

# Display players and their guesses
def DisplayGuess():
    for i in range(len(displayGuessesList)-1, -1, -1):
        displayGuessesList[i].destroy()
        displayGuessesList.pop(i)
    for i in range(len(players)):
        displayGuessesList.append(ttk.Label(frame5, text = f"{players[i].name}'s guess: {players[i].guess}"))
        displayGuessesList[i].grid(row=0, column=i)

def DisplayScore():
    for i in range(len(displayScoreList)-1, -1, -1):
        displayScoreList[i].destroy()
        displayScoreList.pop(i)
    for i in range(len(players)):
        displayScoreList.append(ttk.Label(frame5, text = f"{players[i].name}'s score: {players[i].score}"))
        displayScoreList[i].grid(row = 2, column = i)

def afterGetWins(*args):
    # Destroy the previous frames
    frame3.grid_remove()
    frame4.grid_remove()
    # Display frame 5
    frame5.grid(row = 0, column = 0)
    # Display the trump card
    DisplayTrump()
    # Display everyone's guess
    DisplayGuess()
    # Display everyone's score
    DisplayScore()
    # Set prevStart to the person starting this round
    global prevStart
    global curPlayer
    prevStart = curPlayer
    # First make sure the 1st player is the 1st player
    passTo5()

#display players and their wins
def DisplayWins():
    for i in range(len(displayWinsList)-1, -1, -1):
        displayWinsList[i].destroy()
        displayWinsList.pop(i)
    for i in range(len(players)):
        displayWinsList.append(ttk.Label(frame5, text = f"{Player.name(players[i])}'s wins {Player.wins(players[i])}:"))
        displayWinsList[i].grid(row=1, column=i, padx = 5, pady = 5)
        

#display the players and their picked card
def DisplayPlayed():
    for i in range(len(prevPlaysList)-1, -1, -1):
        prevPlaysList[i].destroy()
        prevPlaysList.pop(i)
    c = 0
    for i in range(len(players)):
        prevPlaysList.append(ttk.Label(frame5, text = f"{players[i].name} played: "))
        prevPlaysList[c].grid(row=4, column=i*2, padx = 5, pady = 5)
        c += 1
        if Player.hasPicked(players[i]):
            prevPlaysList.append(ttk.Label(frame5, image = f"{Player.picked(players[i]).photoImage()}"))
            prevPlaysList[c].grid(row=4, column=(i*2)+1, padx = 5, pady = 5)
            c += 1
    

#display the current hand
def DisplayCurHand():
    global curPlayer
    global cardsLeft
    for i in range(len(cardsLeft)-1, -1, -1):
        cardsLeft[i].destroy()
        cardsLeft.pop(i)
    c = 0
    for i in Player.cards(players[curPlayer]):
        cardsLeft.append(Radiobutton(frame5, image = f"{i.photoImage()}", value=c, indicator=0, height = 120, width = 85, variable = cardPicked))
        cardsLeft[c].grid(row=6, column=c+1)
        c += 1

def deleteLastRound():
    prevRoundLabel.grid_remove()
    for i in range(len(prevRoundList)-1, -1, -1):
        prevRoundList[i].destroy()
        prevRoundList.pop(i)

def displayLastRound():
    prevRoundLabel.grid(row = 8, column = 0, padx = 5, pady = 5)
    for i in range(len(players)):
        prevRoundList.append(ttk.Label(frame5, text = f"{Player.name(players[i])} played:"))
        prevRoundList[2*i].grid(row = 9, column = 2*i, padx = 5, pady = 5)
        prevRoundList.append(ttk.Label(frame5, image = Player.picked(players[i]).photoImage()))
        prevRoundList[(2*i)+1].grid(row = 9, column = (2*i)+1, padx = 5, pady = 5)
    

#this function display the widgets and such of frame 5
def DisplayFrame5(*args):
    global curPlayer
    # Put frame 5 on the grid
    frame5.grid(row = 0, column = 0)
    # Remove frame 6 from the grid
    frame6.grid_remove()
    # Display everyone's wins
    DisplayWins()
    # Display what everyone's played
    DisplayPlayed()
    # Display Your hand
    DisplayCurHand()
    # Remove invalid choiice label from the grid
    invalidChoice.grid_remove()
    # Set current player label
    curPlayerLabel["text"] = f"Current Player: {Player.name(players[curPlayer])}"
    global notFirstRound
    deleteLastRound()
    if notFirstRound:
        displayLastRound()
    # Set Enter key to command getCard
    root.bind('<Return>', getCard)

def validCard(playerCards, pickedCard, startCard, start):
    global trumpCard
    global trumpOut
    if start:
        if Card.suit(pickedCard) != Card.suit(trumpCard) or trumpOut:
            return True
        for card in playerCards:
            if Card.suit(card) != Card.suit(trumpCard):
                return False
        return True
    if Card.suit(pickedCard) == Card.suit(startCard):
        return True
    for card in playerCards:
        if Card.suit(card) == Card.suit(startCard):
            return False
    return True

#get the card selected by the player
def getCard(*args):
    global index5
    global curPlayer
    global cardsLeft
    global counterGetCard
    global startCard
    try:
        i = int(cardPicked.get())
        if counterGetCard == 0:
            startCard = Player.cards(players[curPlayer])[i]
        if validCard(Player.cards(players[curPlayer]), Player.cards(players[curPlayer])[i], startCard, counterGetCard == 0):
            if Card.suit(Player.cards(players[curPlayer])[i]) == Card.suit(trumpCard):
                global trumpOut
                trumpOut = True
            #deselect the card
            cardsLeft[i].deselect()
            #put the card in the player's cards stack
            players[curPlayer].pickCard((Player.cards(players[curPlayer])[i]))
            #pop the card from the player's deck
            players[curPlayer].cards.pop(i)
            #increment curPlayer
            nextPlayer()
            counterGetCard += 1
            if counterGetCard == len(players):
                resetRound()
            else:
                passTo5()
        else:
            invalidChoice.grid(row = 5, column = 4, padx = 5, pady = 5, columnspan = 2)
    except(ValueError):
        pass

def win(card1, card2, trumpSuit):
    if Card.suit(card1) == Card.suit(card2):
        return Card.value(card1) > Card.value(card2)
    if Card.suit(card1) == trumpSuit:
        return True
    return False

def getWinner(players, trumpSuit):
    global prevStart
    winner = prevStart
    for c in range(len(players)):
        if win(Player.picked(players[c]), Player.picked(players[winner]), trumpSuit):
            winner = c
    global curPlayer
    curPlayer = winner
    prevStart = winner
    Player.addWin(players[winner])

def noCardsLeft(players):
    for player in players:
        if len(Player.cards(player)) != 0:
            return False
    return True

def resetRound(*args):
    global counterGetCard
    global notFirstRound
    counterGetCard = 0
    getWinner(players, Card.suit(trumpCard))
    for player in players:
        Player.resetPickedCard(player)
    if noCardsLeft(players):
        for player in players:
            if Player.guess(player) == Player.wins(player):
                Player.addScore(player, Player.guess(player) + 10)
            Player.resetWin(player)
        global trumpOut
        trumpOut = False
        frame5.grid_remove()
        global roundNum
        roundNum -= 1
        notFirstRound = False
        if roundNum == 0:
            EndGame()
        else:
            outerGameLoop()
    else:
        notFirstRound = True
        passTo5()
                
    
#make sure the current player is the right player before continuing
def passTo5():
    global curPlayer
    if curPlayer == int(numPlayers.get()):
        NextScreen()
    else:
        # Stop displaying frame 5
        frame5.grid_remove()
        # Display frame 6
        frame6.grid(row = 0, column = 0)
        #Set name of player in appropriate widgets
        playerPass6["text"] = "Pass to " + Player.name(players[curPlayer])
        enter6["text"] = "I am " + Player.name(players[curPlayer])
        # Set Enter key to command for after pass
        root.bind('<Return>', DisplayFrame5)
        # Set button command for after pass
        enter6["command"] = DisplayFrame5

def sortPlayers():
    for c in range(len(players)):
        maximum = c
        for i in range(c+1, len(players)):
            if Player.score(players[i]) > Player.score(players[maximum]):
                maximum = i
        players[maximum], players[c] = players[c], players[maximum]

def displayFinalScores():
    for c in range(len(players)):
        print(f"{Player.name(players[c])}'s score: {Player.score(players[c])}")
        ttk.Label(frame7, text = f"{Player.name(players[c])}'s score: {Player.score(players[c])}").grid(row = c+1, column = 0)
    for child in frame7.winfo_children(): child.grid_configure(padx=5, pady=5)
    
#test screan for the next part
def EndGame():
    # Display frame 7
    frame7.grid(row = 0, column = 0)
    # Sort Players by score
    sortPlayers()
    # Display final scores
    displayFinalScores()

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
# Variable to hold who started the previous round
prevStartPlayer = 0
# Variable to hold trump card
trumpCard = Card(0)
# List to hold the card widgets that are used in frame 3
cardDisplay = []
# Counter for frame 3
counter3 = 0
# Create a list for previous players guesses
prevGuesses = []
#the card picked in frame 5
cardPicked = StringVar()
#index for displaying cards in frame 5
index5 = 0
#hold the card buttons in frame 5
cardsLeft = []
# Create a counter for getting cards
counterGetCard = 0
# List to hold widgets for displaying guesses
displayGuessesList = []
# List to hold widgets for displaying wins
displayWinsList = []
# List to hold widgets for displaying what the previous players played
prevPlaysList = []
# Variable to hold who started the round
prevStart = 0
# Variable to hold what card was the starting card
startCard = Card(0)
# Variable to hold whether a trump has gone out yet
trumpOut = False
# Variable to hold player scores
displayScoreList = []
# List to hold score during guesss phase
guessScoreList = []
# List to hold cards played in the previous round
prevRoundList = []
# Boolean to say if not the round is the first round
notFirstRound = False

# Frame1: Get number of players
frame1 = ttk.Frame(root, padding = "3 3 12 12")
frame1.grid(column=0, row=0, )
# Label for number of players
numlabel = ttk.Label(frame1, text = "Number of Players:")
numlabel.grid(row = 0, column = 0)
# Number of players entry box
numEntry = ttk.Entry(frame1, textvariable = numPlayers)
numEntry.grid(row=0, column=1)
# Create an "Enter!" button and go to the next screen
Enter = ttk.Button(frame1, text = "Enter!", command = checkNumPlayers) 
Enter.grid(row=1, column=1)
# Create spacing around each widget
for child in frame1.winfo_children(): child.grid_configure(padx=5, pady=5)
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
for child in frame2.winfo_children(): child.grid_configure(padx=5, pady=5)

# Frame3: Get the number of wins for the round
frame3 = ttk.Frame(root, padding = "3 3 12 12")
# Create the widgets for screen 3:
# Label to ask how many cards a player will win
winLabel = ttk.Label(frame3)
winLabel.grid(row = 0, column = 0, columnspan = 2)
# Create an entry box for players to input how many cards they wilil win
winEntry = ttk.Entry(frame3, textvariable = getWins)
winEntry.grid(row=0, column=2)
# Create an "Enter!" button and go to the next screen
Enter3 = ttk.Button(frame3, text = "Enter!", command = getNumWins) 
Enter3.grid(row=1, column=2)
# Create label to say what round we are on
roundNumLabel = ttk.Label(frame3)
roundNumLabel.grid(row = 1, column = 0, columnspan = 2)
# Create label to say what the player's cards are
playerCardLabel = ttk.Label(frame3, text = "Your cards:")
playerCardLabel.grid(row = 3, column = 0)
# Create label for trump card
trumpCardLabel = ttk.Label(frame3, text = "Trump card:")
trumpCardLabel.grid(row = 2, column = 0)
# Create label for trump card image
trumpCardImage = ttk.Label(frame3)
trumpCardImage.grid(row = 2, column = 1)
# Spacing around each widget
for child in frame3.winfo_children(): child.grid_configure(padx=5, pady=5)

# Frame4: pass to screen
frame4 = ttk.Frame(root, padding = "3 3 12 12")
# Create the widgets for screen 4:
# Create Label to say who to pass to
playerPass = ttk.Label(frame4)
playerPass.grid(row = 0, column = 0)
# Create button to press
confirmPlayer = ttk.Button(frame4)
confirmPlayer.grid(row = 0, column = 1)
for child in frame4.winfo_children(): child.grid_configure(padx=5, pady=5)

#Frame5: Pick cards
frame5 = ttk.Frame(root, padding = "3 3 12 12")
# Create the widgets for screen 5:
# Create button to press
enter5 = ttk.Button(frame5, text = "Pick this card!", command = getCard)
enter5.grid(row = 7, column = 0)
trumpCard5 = ttk.Label(frame5, text = "Trump Card:")
trumpCard5.grid(row=5, column=0)
trumpImage5 = ttk.Label(frame5)
trumpImage5.grid(row=5, column=1)
yourCards5 = ttk.Label(frame5, text = "Your cards:")
yourCards5.grid(row=6, column=0)
curPlayerLabel = ttk.Label(frame5)
curPlayerLabel.grid(row = 5, column = 2, columnspan = 2)
invalidChoice = ttk.Label(frame5, text = "Invalid Card, try again")
prevRoundLabel = ttk.Label(frame5, text = "Previous round:")
for child in frame5.winfo_children(): child.grid_configure(padx=5, pady=5)

#Frame6: Pass to next player
frame6 = ttk.Frame(root, padding = "3 3 12 12")
# Create Label to say who to pass to
playerPass6 = ttk.Label(frame6)
playerPass6.grid(row = 0, column = 0)
# Create button to press
enter6 = ttk.Button(frame6)
enter6.grid(row = 0, column = 1)

for child in frame6.winfo_children(): child.grid_configure(padx=5, pady=5)

# Frame7: Win Screen
frame7 = ttk.Frame(root, padding = "3 3 12 12")
# Create Label to say what the score is
finalScore = ttk.Label(frame7, text = "Final Score:")
finalScore.grid(column = 0, row = 0)

root.mainloop()
