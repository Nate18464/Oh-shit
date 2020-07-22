from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import random

#Create root window to show the screen and title it Oh Shit!
root = Tk()
root.title("Oh Shit!")

counter = 0
#This is the second screen, where the screen will repeatedly take in names for each player
def secondScreen(*args):
    root.bind('<Return>', secondScreen)
    nameEntry.focus()
    #destroy the first screen
    frame1.destroy()
    #for the number of players
    nameEntry.delete(0, "end")
    global counter

    counter = counter + 1
    nameLabel.configure(text=f'Name of player {counter}')
    if counter != int(numPlayers.get()):
        playerNames.append(getName.get())
        
    else:
        playerNames.append(getName.get())
        root.bind('<Return>', thirdScreen)
        Enter2["command"] = thirdScreen
    


#testing screen
def thirdScreen(*args):
    frame2.destroy() 
    print("in 3rd screen")

        
#Frame1: Get the number of players
frame1 = ttk.Frame(root, padding = "3 3 12 12")
frame1.grid(column=0, row=0, stick=(N,W,E,S))

#Frame2: Get the names of the players
frame2 = ttk.Frame(root, padding = "3 3 12 12")
frame2.grid(column=0, row=0, sticky=(N, W, E, S))

# Lower this second frame below the first frame
frame2.lower(frame1)


#list of players and their names, to be filled in SecondScreen
playerNames = []

#Create the widgets for screen 1

#numPlayers label
numlabel = ttk.Label(frame1, text = "Number of Players: ").grid(row = 0, column = 0, sticky = (N, W, E, S))
#create a variable to hold the number of players
numPlayers = StringVar()
numEntry = ttk.Entry(frame1, textvariable = numPlayers)
numEntry.grid(row=0, column=1, sticky = (N, W, E, S))
#Create an "Enter!" button and go to the next screen
Enter = ttk.Button(frame1, text = "Enter!", command = secondScreen) 
Enter.grid(row=1, column=1, sticky = (N, W, E, S))

#spacing around each widget
for child in frame1.winfo_children(): child.grid_configure(padx=5, pady=5)


#Create the widgets for screen 2:

#namePlayers label
nameLabel = ttk.Label(frame2, text = "What's your name, player ")
nameLabel.grid(row = 0, column = 0, sticky = (N, W, E, S))
#create a variable to hold the name of players
getName = StringVar()
nameEntry = ttk.Entry(frame2, textvariable = getName)
nameEntry.grid(row=0, column=1, sticky = (N, W, E, S))
#Create an "Enter!" button and go to the next screen
Enter2 = ttk.Button(frame2, text = "Enter your name!", command = secondScreen) 
Enter2.grid(row=1, column=1, sticky = (N, W, E, S))


#State with the cursor in the textbot
numEntry.focus()
#Bind return to also bring us to the next screen
root.bind('<Return>', secondScreen)


#spacing around each widget
for child in frame2.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()
