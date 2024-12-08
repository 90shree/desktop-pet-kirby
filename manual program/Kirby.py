import tkinter as tk
import time
import random
import pygetwindow as gw


class Kirby:
    def __init__(self):
        self.window = tk.Tk()
        self.window.config(bg='purple')  
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.wm_attributes('-transparentcolor', 'purple')

        self.load_gifs()
        self.init_variables()

        self.label = tk.Label(self.window, bd=0, bg='purple')  
        self.label.pack(side='bottom', anchor='s')  


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
        self.sleep = [tk.PhotoImage(file='sleep.gif', format='gif -index %i' % i) for i in range(3)]
        self.eat = [tk.PhotoImage(file='eat.gif', format='gif -index %i' % i) for i in range(12)]
        self.walk_left = [tk.PhotoImage(file='walkleft.gif', format='gif -index %i' % i) for i in range(10)]
        self.walk_right = [tk.PhotoImage(file='walkright.gif', format='gif -index %i' % i) for i in range(10)]
        self.idle = [tk.PhotoImage(file='idle.gif', format='gif -index %i' % i) for i in range(4)]
        self.idle2 = [tk.PhotoImage(file='idle2.gif', format='gif -index %i' % i) for i in range(48)]
        self.fall = [tk.PhotoImage(file='fall.gif', format='gif -index %i' % i) for i in range(20)]
        self.hold = [tk.PhotoImage(file='hold.gif', format='gif -index %i' % i) for i in range(5)]  


    def init_variables(self):
        self.current_action = 'idle'
        self.img = self.idle[0]

        self.x = (self.window.winfo_screenwidth() - 110) / 2
        self.y = self.window.winfo_screenheight() - 100

        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.0981
        self.last_action_time = time.time()
        self.last_change_time = time.time()
        self.action_duration = 0
        self.is_falling = False
        self.idle_time = 50
        self.ground_level = self.window.winfo_screenheight() - 147

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
        current_time = time.time()

        if self.dragging:
            self.current_action = 'hold'
            self.img_sequence = self.hold  
            frame_interval = 0.1  

            frame_index = int(((current_time - self.last_action_time) / frame_interval) % len(self.img_sequence))
            self.img = self.img_sequence[frame_index]

        else:
            self.update_movement()

        self.update_window()

        self.window.after(10, self.update)
        
    def update_movement(self):
        current_time = time.time()

        if not self.dragging:
            self.vel_y += self.gravity
            self.y += self.vel_y

            if self.y >= self.ground_level:
                self.y = self.ground_level
                self.vel_y = 0
                self.is_falling = False
            else:
                self.is_falling = True

            window = self.check_near_window()
            if window:
                self.y = window.top - 100
                self.vel_y = 0
                self.is_falling = False

                if self.current_action == 'walk_left' and self.x > window.left + 10:
                    self.x -= 0.5
                elif self.current_action == 'walk_right' and self.x + 100 < window.right - 10:
                    self.x += 0.9
                else:
                    if self.current_action == 'walk_left':
                        self.x += 0.5
                        self.start_walking('walk_right')
                    elif self.current_action == 'walk_right':
                        self.x -= 2
                        self.start_walking('walk_left')

            if self.is_falling:
                if self.current_action != 'fall':
                    self.current_action = 'fall'
                    self.img_sequence = self.fall
                    self.last_action_time = current_time
            elif self.current_action == 'fall':
                self.current_action = 'idle'
                self.img_sequence = self.idle
                self.last_action_time = current_time

            if not self.is_falling and self.current_action == 'idle':
                if current_time > self.last_change_time + self.idle_time:
                    self.last_change_time = current_time
                    random_action = random.randint(1, 5)

                    if random_action == 1:
                        self.current_action = 'sleep'
                        self.img_sequence = self.sleep
                        self.action_duration = 10
                    elif random_action == 2:
                        self.current_action = 'eat'
                        self.img_sequence = self.eat
                        self.action_duration = 6
                    elif random_action in [3, 4]:
                        direction = 'walk_right' if random_action == 3 else 'walk_left'
                        self.start_walking(direction)
                        self.action_duration = 10
                    elif random_action == 5:
                        self.current_action = 'idle2'
                        self.img_sequence = self.idle2
                        self.action_duration = 20

                    self.last_action_time = current_time

            if self.current_action == 'walk_left':
                if window:
                    if self.x > window.left + 10:
                        self.x -= 0.5
                    else:
                        self.x += 0.5
                        self.start_walking('walk_right')
                elif self.x <= 0:
                    self.x += 0.5
                    self.start_walking('walk_right')
                else:
                    self.x -= 0.5

            elif self.current_action == 'walk_right':
                if window:
                    if self.x + 100 < window.right - 10:
                        self.x += 0.9
                    else:
                        self.x -= 2
                        self.start_walking('walk_left')
                elif self.x + 100 >= self.window.winfo_screenwidth():
                    self.x -= 2
                    self.start_walking('walk_left')
                else:
                    self.x += 0.9

            if hasattr(self, 'img_sequence') and self.current_action:
                num_frames = len(self.img_sequence)
                frame_interval = 0.25

                if self.current_action in ['walk_left', 'walk_right']:
                    frame_interval = 0.1
                elif self.current_action == 'sleep':
                    frame_interval = 0.35
                elif self.current_action == 'idle2':
                    frame_interval = 0.15
                elif self.current_action == 'fall':
                    frame_interval = 0.1
                elif self.current_action == 'eat':
                    frame_interval = 0.15

                frame_index = int(((current_time - self.last_action_time) / frame_interval) % num_frames)
                self.img = self.img_sequence[frame_index]

            if current_time > self.last_action_time + self.action_duration:
                if self.current_action != 'idle' and not self.is_falling:
                    self.current_action = 'idle'
                    self.img_sequence = self.idle
                    self.action_duration = 20
                    self.last_action_time = current_time


    def start_walking(self, direction):
        self.current_action = direction
        self.img_sequence = self.walk_right if direction == 'walk_right' else self.walk_left
        self.action_duration = random.randint(10, 11) * len(self.img_sequence) * 0.1


    def check_near_window(self):
        for win in self.get_open_windows():
            if (
                self.x + 35 > win.left and
                self.x + 35 < win.right and
                self.y + 100 >= win.top and
                self.y + 100 <= win.top + 15
            ):
                return win
        return None

    def get_open_windows(self):
        windows = []
        for win in gw.getWindowsWithTitle(''):
            if win.visible and win.width > 100 and win.height > 100:
                windows.append(win)
        return windows

    def update_window(self):
        self.window.geometry('100x100+{x}+{y}'.format(x=str(int(self.x)), y=str(int(self.y))))
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

    def release_drag(self, event):
        self.dragging = False




Kirby()
