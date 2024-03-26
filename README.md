# Demo



![ezgif-4-fec92e5b61](https://github.com/90shree/desktop-pet-kirby/assets/163702108/6ba6b5e8-f85a-44d7-891f-ea971db11e17)


A desktop pet Kirby companion created with Python! It eats (inhales), occasionally sleep and walk/flies around the bottom of your desktop screen.
Also draggable with fall/gravity mechanics!

The art is not mine. 

# How was it made?
The program is essentially a series of gif-animations ontop of a fitted transparent window, made with the help of the Python module "tkinter" to manipulate GUI aspects of the window. Object Oriented Programming was used to define the window as its own class, and each animation was also drawn by hand using a pixel-art program, then converted into readable gif files. 

The program picks a random action to preform every seven seconds, while displaying an idle animation in between. 

Gravity/Drop physics was implemented through declaring variables for velocity, acceleration and gravity.. then adding the gravity variable to the y-velocity (using a plus-equals operator) when the user is not dragging the window, and applying this logic to both acceleration and velocity as well.



# How to run
Simply extract the 'Kirby.zip' file and run the python executable :)

***Right click Kirby and select "Close Kirby" to close the program!*

# If, for any reason, this is not possible:

You will have to run the program using the assets in the "manual program" folder. Follow the steps below to do so.

## 1. Ensure that you have Python 3 installed.

## 2. Install the necessary modules needed to run this program with the following commands:

'pip install tk'

'pip install win32gui'

'pip install random'

## 3. Now you can run the program in Command prompt by:

First changing the directory to where this program is stored by using the 'cd' command, followed by a space, then your directory.

Then simply the command, "Kirby.py"
