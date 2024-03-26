import tkinter as tk
import time
import random
import win32gui

class Kirby:
    def __init__(self):
        self.window = tk.Tk()
        self.window.config(highlightbackground='purple')
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.wm_attributes('-transparentcolor', 'purple')

        self.load_gifs()

        self.init_variables()

        self.label = tk.Label(self.window, bd=0, bg='purple')
        self.label.pack()

        self.dragging = False
        self.start_x = 0
        self.start_y = 0

        self.label.bind("<ButtonPress-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.drag)
        self.label.bind("<ButtonRelease-1>", self.release_drag)

        self.label.bind("<Button-3>", self.right_click_menu)

        self.update()
        self.window.mainloop()

    def load_gifs(self):
        self.phone = [tk.PhotoImage(file='phone.gif', format='gif -index %i' % i) for i in range(4)]
        self.eat = [tk.PhotoImage(file='eat.gif', format='gif -index %i' % i) for i in range(12)]
        self.walk_left = [tk.PhotoImage(file='walkleft.gif', format='gif -index %i' % i) for i in range(10)]
        self.walk_right = [tk.PhotoImage(file='walkright.gif', format='gif -index %i' % i) for i in range(10)]
        self.idle = [tk.PhotoImage(file='idle.gif', format='gif -index %i' % i) for i in range(1)]
        self.fall = [tk.PhotoImage(file='fall.gif', format='gif -index %i' % i) for i in range(20)]

    def init_variables(self):
        self.current_action = None
        self.img = self.idle[0]
        self.taskbar_height = self.get_taskbar_height()
        self.default_y = self.window.winfo_screenheight() - self.taskbar_height - 70
        self.y = self.default_y
        self.x = (self.window.winfo_screenwidth() - 110) / 2
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.0981
        self.last_action_time = time.time()
        self.last_change_time = time.time()
        self.action_duration = 0
        self.moving_back = False
        self.is_falling = False 

    def get_taskbar_height(self):
        hwnd = win32gui.FindWindow("Shell_traywnd", None)
        rect = win32gui.GetWindowRect(hwnd)
        return rect[3] - rect[1]

    def right_click_menu(self, event):
        menu = tk.Menu(self.window, tearoff=0)
        menu.add_command(label="Close Kirby", command=self.close_program)
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def close_program(self):
        self.window.destroy()

    def update(self):
        self.update_movement()
        self.update_window()
        self.window.after(10, self.update)

    def update_movement(self):
        current_time = time.time()
        
        if not self.dragging:
            self.vel_y += self.gravity
            self.y += self.vel_y
            if self.y >= self.default_y:
                self.y = self.default_y
                self.vel_y = 0
                if self.is_falling:
                    self.current_action = 'idle'
                    self.img_sequence = self.idle
                    self.is_falling = False
            elif self.y < self.default_y and not self.is_falling:
        
                self.is_falling = True
                self.current_action = 'fall'
                self.img_sequence = self.fall
                self.action_duration = len(self.fall) * 1

        
        
        if hasattr(self, 'img_sequence') and self.current_action:
            num_frames = len(self.img_sequence)
            frame_index = int(((current_time - self.last_action_time) / 0.1) % num_frames)
            self.img = self.img_sequence[frame_index]

        if current_time > self.last_action_time + self.action_duration:
        
            self.current_action = 'idle'
            self.img_sequence = self.idle 
            self.action_duration = 0
            self.last_action_time = current_time 
        

        
        if current_time > self.last_change_time + 7 and not self.moving_back and self.current_action in ['idle', None] and not self.is_falling:
            self.last_change_time = current_time
            random_action = random.randint(1, 4)
            if random_action == 1:
                self.current_action = 'phone'
                self.img_sequence = self.phone
                self.action_duration = len(self.phone) * 1 
            elif random_action == 2:
                self.current_action = 'eat'
                self.img_sequence = self.eat
                self.action_duration = len(self.eat) * 1
            elif random_action == 3 or random_action == 4:
                direction = 'walk_right' if random_action == 3 else 'walk_left'
                self.start_walking(direction)
                self.action_duration = 9  

            self.last_action_time = current_time

        # movement
        if self.current_action == 'walk_right':
            if not self.moving_back and self.x > self.window.winfo_screenwidth() - 70:
                self.start_moving_back('left')
            else:
                self.x += 1
        elif self.current_action == 'walk_left':
            if not self.moving_back and self.x < 0:
                self.start_moving_back('right')
            else:
                self.x -= 1

    def start_walking(self, direction):
        self.current_action = direction
        self.img_sequence = self.walk_right if direction == 'walk_right' else self.walk_left
        self.action_duration = random.randint(5, 7) * len(self.img_sequence) * 0.1

    def start_moving_back(self, direction):
        self.moving_back = True
        self.start_walking('walk_right' if direction == 'right' else 'walk_left')
        self.action_duration = 5

    def update_window(self):
        self.window.geometry('70x70+{x}+{y}'.format(x=str(int(self.x)), y=str(int(self.y))))
        self.label.configure(image=self.img)

    def start_drag(self, event):
        self.dragging = True
        self.start_x = event.x_root
        self.start_y = event.y_root

    def drag(self, event):
        if self.dragging:
            self.x = event.x_root - self.start_x + self.x
            self.y = event.y_root - self.start_y + self.y
            self.start_x = event.x_root
            self.start_y = event.y_root

            self.current_action = None
            self.is_falling = False

    def release_drag(self, event):
        self.dragging = False


Kirby()
