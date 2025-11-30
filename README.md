# Demo


Real-time Uncut Demo:

https://github.com/user-attachments/assets/b9e87a8c-0ce9-4d17-9aec-5efbeabf8e3e







A desktop pet Kirby companion created with Python. It eats (inhales), occasionally sleep and walk/flies around the bottom of your desktop screen. It's draggable, throwable and can sit ontop of windows and preform all animations without falling off. When thrown, it detects the user's screen boundaries and will bounce within the boundaries before coming to rest, simulating realistic physics mechanisms.

(The art is not mine.)

# How was it made?

I designed the system around a custom animation loop that updates every 10 ms. Each Kirby action (walk, idle, sleep, etc.) is represented by a sequence of GIF frames in a fitted transparent window. The program switches between these frame sequences dynamically based on Kirby’s movement state or scheduled behaviors. A timing system controls animation speed and randomly selects new actions at intervals to make the pet feel more alive.

Kirby moves around the screen under simple physics: gravity, horizontal velocity, friction, and collision detection with screen boundaries. When dragged and released, Kirby inherits velocity calculated from the user’s drag motion, allowing the pet to “throw” and bounce naturally across the screen.

The interface uses a transparent, borderless Tkinter window pinned above all other windows. Kirby can be dragged around with the mouse, and a right-click opens a small contextual menu to close the program.

## The physics

The physics system for the desktop pet is built entirely from scratch by tracking Kirby’s position and velocity on both the horizontal and vertical axes and updating them in small time steps. 

- Gravity is implemented by increasing Kirby’s vertical velocity a little bit on every frame of the update loop; because the update loop runs very frequently, this repeated increment creates the effect of continuous downward acceleration. That velocity is then added to Kirby’s vertical position each frame, causing him to fall.
- Throwability is achieved by recording a short history of the mouse’s positions while the user is dragging Kirby. 

When the drag ends, the system compares the last two recorded positions and the time between them in order to calculate an approximate release velocity. That calculated velocity becomes Kirby’s new horizontal and vertical speeds, letting him continue to move in the direction and speed of the user’s flick. Bounciness is handled by detecting when Kirby reaches the floor or hits a horizontal boundary. 

When that happens, his velocity along the impacted axis is reversed and scaled down by a multiplier less than one, which simulates energy loss and makes each bounce progressively smaller. Additionally, when Kirby is on the ground and not walking, the horizontal velocity is gradually reduced by multiplying it by a friction factor each frame, causing him to slow to a stop rather than slide indefinitely. 

All of these elements, gravity updates, velocity-based motion, drag-release velocity calculation, boundary collision checks, bounce scaling, and ground friction, combine to form a simple but fully custom physics model that drives Kirby’s movement.


# How to run
Simply open the contents within the "executable" folder, and run the "Kirby.exe" executable.

Temporarily turn off virus detection while downloading and extracting the file if it is being flagged as a virus.

***Right click Kirby and select "Close Kirby" to close the program*


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
