from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import random

#Create root window to show the screen and title it Oh Shit!
root = Tk()
root.title("Oh Shit!")

#this counter variable is for keeping track of how many times the screen has cycled through
counter2 = 1
#This is the second screen, where the screen will repeatedly take in names for each player
def secondScreen(*args):
    root.bind('<Return>', secondScreen)
    nameEntry.focus()
    #destroy the first screen
    frame1.destroy()
    global counter2

    nameLabel.configure(text=f'Name of player {counter2}')

    if getName.get() != '':
        playerNames.append(getName.get())
        if counter2 == int(numPlayers.get())-1:
            root.bind('<Return>', thirdScreen)
            Enter2["command"] = thirdScreen
        #clear the entry box
        nameEntry.delete(0, "end")
        counter2 += 1
        nameLabel.configure(text=f'Name of player {counter2}')        
            

counter3 = 0
#This is where the screen where repeated take wins for each player
def thirdScreen(*args):
    root.bind('<Return>', thirdScreen)
    winEntry.focus()
    #add the last name
    playerNames.append(getName.get())
    #destroy the second screen
    frame2.destroy()
    global counter3

    #display the name of the player on the label
    name = playerNames[counter3]
    winLabel.configure(text=f"Player {name} wins: ")

    if getWins.get() != '':
        if counter3 == int(numPlayers.get())-2:
            root.bind('<Return>', fourthScreen)
            Enter3["command"] = fourthScreen
        winsInt = int(getWins.get())
        wins.append(winsInt)
        #clear the entry box
        winEntry.delete(0, "end")
        counter3 += 1
        name = playerNames[counter3]
        winLabel.configure(text=f"Player {name} wins: ")



def fourthScreen(*args):
    #add that last value to getWins
    winsInt = int(getWins.get())
    wins.append(winsInt)
    #destroy the third screen
    frame3.destroy()

        
#Frame1: Get the number of players
frame1 = ttk.Frame(root, padding = "3 3 12 12")
frame1.grid(column=0, row=0, stick=(N,W,E,S))

#Frame2: Get the names of the players
frame2 = ttk.Frame(root, padding = "3 3 12 12")
frame2.grid(column=0, row=0, sticky=(N, W, E, S))

# Lower this second frame below the first frame
frame2.lower(frame1)

#Frame3: Get the number of wins for the round
frame3 = ttk.Frame(root, padding = "3 3 12 12")
frame3.grid(column=0, row=0, sticky=(N, W, E, S))

# Lower this third frame below the second frame
frame3.lower(frame2)

#variables:
#list of players and their names, to be filled in SecondScreen
playerNames = []
#list of players and their wins, to be filled in thirdScreen
wins = []
#create a variable to hold the number of players
numPlayers = StringVar()
#create a variable to hold the name of players
getName = StringVar()
#create a variable to hold the number of wins
getWins = StringVar()


#Create the widgets for screen 1
#numPlayers label
numlabel = ttk.Label(frame1, text = "Number of Players: ").grid(row = 0, column = 0, sticky = (N, W, E, S))
#number of players entry
numEntry = ttk.Entry(frame1, textvariable = numPlayers)
numEntry.grid(row=0, column=1, sticky = (N, W, E, S))
#Create an "Enter!" button and go to the next screen
Enter = ttk.Button(frame1, text = "Enter!", command = secondScreen) 
Enter.grid(row=1, column=1, sticky = (N, W, E, S))
#spacing around each widget
for child in frame1.winfo_children(): child.grid_configure(padx=5, pady=5)

#State with the cursor in the textbot
numEntry.focus()
#Bind return to also bring us to the next screen
root.bind('<Return>', secondScreen)


#Create the widgets for screen 2:
#namePlayers label
nameLabel = ttk.Label(frame2, text = "What's your name, player ")
nameLabel.grid(row = 0, column = 0, sticky = (N, W, E, S))
#name entry
nameEntry = ttk.Entry(frame2, textvariable = getName)
nameEntry.grid(row=0, column=1, sticky = (N, W, E, S))
#Create an "Enter!" button and go to the next screen
Enter2 = ttk.Button(frame2, text = "Enter!", command = secondScreen) 
Enter2.grid(row=1, column=1, sticky = (N, W, E, S))
#spacing around each widget
for child in frame2.winfo_children(): child.grid_configure(padx=5, pady=5)


#Create the widgets for screen 3:
#wins label
winLabel = ttk.Label(frame3, text = "How many wins? ")
winLabel.grid(row = 0, column = 0, sticky = (N, W, E, S))
#win entry
winEntry = ttk.Entry(frame3, textvariable = getWins)
winEntry.grid(row=0, column=1, sticky = (N, W, E, S))
#Create an "Enter!" button and go to the next screen
Enter3 = ttk.Button(frame3, text = "Enter!", command = thirdScreen) 
Enter3.grid(row=1, column=1, sticky = (N, W, E, S))
#spacing around each widget
for child in frame3.winfo_children(): child.grid_configure(padx=5, pady=5)




root.mainloop()
