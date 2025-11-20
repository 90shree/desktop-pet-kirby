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
        self.gravity = 0.25
        self.bounce_factor = 0.7
        self.side_bounce_factor = 0.8

        self.last_drag_positions = []
        self.max_drag_samples = 5

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

        # physics floor collision
        if self.y >= self.ground_level:
            self.y = self.ground_level  # position Kirby just above the ground

            # Invert vertical velocity for bounce
            if self.vel_y > 0:  # only if moving downward
                self.vel_y = -self.vel_y * self.bounce_factor

            self.is_falling = True  # still falling after bounce

            # Apply horizontal friction only if on ground
            if abs(self.vel_x) > 0:
                self.vel_x *= 0.85
                if abs(self.vel_x) < 0.1:
                    self.vel_x = 0


        if not self.dragging:
            self.vel_y += self.gravity
            self.y += self.vel_y
            self.x += self.vel_x

            screen_w = self.window.winfo_screenwidth()

            if self.y < 0:
                self.y = 0
                if self.vel_y < 0:
                    self.vel_y = -self.vel_y * self.bounce_factor

            if self.x <= 0:
                self.x = 0
                self.vel_x *= -self.side_bounce_factor

            elif self.x + 100 >= screen_w:
                self.x = screen_w - 100
                self.vel_x *= -self.side_bounce_factor

            if self.vel_y == 0 and abs(self.y - self.ground_level) < 2:
                self.y = self.ground_level
                self.is_falling = False
            else:
                self.is_falling = True

            if self.y >= self.ground_level:
                self.y = self.ground_level
                if abs(self.vel_y) > 1:
                    self.vel_y = -self.vel_y * self.bounce_factor
                else:
                    self.vel_y = 0
                self.is_falling = False

            if self.is_falling:
                if self.current_action != 'fall':
                    self.current_action = 'fall'
                    self.img_sequence = self.fall
                    self.last_action_time = current_time
            else:
                if self.current_action == 'fall':
                    self.current_action = 'idle'
                    self.img_sequence = self.idle
                    self.last_action_time = current_time

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

    def update_window(self):
        self.window.geometry(f'100x100+{int(self.x)}+{int(self.y)}')
        self.label.configure(image=self.img)

    def start_drag(self, event):
        self.dragging = True
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.vel_x = 0
        self.vel_y = 0

        self.last_drag_positions = []

    def drag(self, event):
        if self.dragging:
            dx = event.x_root - self.start_x
            dy = event.y_root - self.start_y

            self.x += dx
            self.y += dy

            self.start_x = event.x_root
            self.start_y = event.y_root

            self.last_drag_positions.append((time.time(), event.x_root, event.y_root))

            if len(self.last_drag_positions) > self.max_drag_samples:
                self.last_drag_positions.pop(0)

    def release_drag(self, event):
        self.dragging = False

        if len(self.last_drag_positions) >= 2:
            t1, x1, y1 = self.last_drag_positions[-2]
            t2, x2, y2 = self.last_drag_positions[-1]
            dt = t2 - t1

            if dt > 0:
                self.vel_x = (x2 - x1) / dt * 0.015
                self.vel_y = (y2 - y1) / dt * 0.015


Kirby()

