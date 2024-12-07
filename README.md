# Demo


Real-time Uncut Demo:

https://github.com/user-attachments/assets/b9e87a8c-0ce9-4d17-9aec-5efbeabf8e3e







A desktop pet Kirby companion created with Python. It eats (inhales), occasionally sleep and walk/flies around the bottom of your desktop screen. It's draggable and can sit ontop of windows and preform all animations without falling off. 

(The art is not mine.)

# How was it made?
The program is essentially a series of gif-animations ontop of a fitted transparent window, made with the help of the Python module "tkinter" to manipulate GUI aspects of the window. Object Oriented Programming was used to define the window as its own class in order to define its own environment and actions. 

The program picks a random action to preform every few seconds, while displaying an idle animation in between. 

Gravity/Drop physics was implemented through declaring variables for velocity, acceleration and gravity.. then adding the gravity variable to the y-velocity in a loop (to simulate gravity's constant downwards force on the window) when the window is falling after being dragged.



# How to run
Simply open the contents within the "executable" folder, and run the "Kirby.exe" executable.

***Right click Kirby and select "Close Kirby" to close the program!*

# If, for any reason, this is not possible:

You will have to run the program using the assets in the "manual program" folder. Follow the steps below to do so.

## 1. Ensure that you have Python 3 installed.

## 2. Install the necessary modules needed to run this program with the following commands:

'pip install tk'

'pip install win32gui'

'pip install random'

'pip install pygetwindow'

## 3. Now you can run the program in Command prompt by:

First changing the directory to where this program is stored by using the 'cd' command, followed by a space, then your directory.

Then simply the command, "Kirby.py"

You can also run the program directly from its IDE.
