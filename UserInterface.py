import pygame
import json
import tkinter as tk
from tkinter import messagebox
import threading
import os

# Load input data
with open("algo_output.json") as f:
    input_data = json.load(f)

# Setting Up Pygame
pygame.init()
width, height = 400, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Elevator Sim 2024")

# For FPS and Frame Capping
clock = pygame.time.Clock()

# Translate the storey into the y-coordinates
storey = {
    1: 442,
    2: 372,
    3: 302,
    4: 232, 
    5: 162,
    6: 92, 
    7: 22
}
background_path = os.path.join("images", "Elevator_background.png")
background = pygame.image.load(background_path)

# Creating Elevator Class 
class Elevator(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_y):
        super(Elevator, self).__init__()
        image_path = os.path.join("images", "elevator", "Elevator_Doors_1.png")
        self.image = pygame.image.load(image_path).convert()
        self.image.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_y = speed_y
        self.target_y = y
        self.is_at_target = False
        self.animation_playing = False
        self.animation_played = False
        self.close_doors = False
        self.doors_closed = False
        self.animation_frames = [
            pygame.image.load(os.path.join("images", "elevator", f"elevator_doors_{i}.png")).convert() for i in range(1, 14)
        ]
        for frame in self.animation_frames:
            frame.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.anim_index = 0

    def update(self):
        if self.rect.y < self.target_y:
            self.rect.y += min(self.speed_y, self.target_y - self.rect.y)
        elif self.rect.y > self.target_y:
            self.rect.y -= min(self.speed_y, self.rect.y - self.target_y)
        if self.rect.y == self.target_y:
            self.is_at_target = True
            if not self.animation_playing and not self.animation_played:
                self.animation_playing = True
                self.anim_index = 0
        else:
            self.is_at_target = False
            self.animation_playing = False
            self.animation_played = False
            self.close_doors = False

    def set_storey(self, target_y):
        self.target_y = target_y
        self.is_at_target = False
        self.animation_playing = False
        self.animation_played = False
        self.close_doors = False

    def play_animation_open_door(self):
        if self.is_at_target and self.animation_playing:
            if self.anim_index < len(self.animation_frames) - 1:
                self.anim_index += 1
                self.image = self.animation_frames[self.anim_index]
            else:
                self.animation_played = True
                self.image = self.animation_frames[-1]
                self.close_doors = True
                self.doors_closed = False

    def play_animation_close_door(self):
        if self.is_at_target and self.close_doors:
            if self.anim_index > 0:
                self.anim_index -= 1
                self.image = self.animation_frames[self.anim_index]
            else:
                self.image = self.animation_frames[0]
                self.doors_closed = True

# Create elevators and group them
all_elevators = pygame.sprite.Group()
elevator1 = Elevator(100, storey[1], 5)
elevator2 = Elevator(184, storey[2], 5)
elevator3 = Elevator(268, storey[3], 5)
all_elevators.add(elevator1, elevator2, elevator3)

# Tkinter Part
def submit_number():
    try:
        number = int(number_entry.get())
        if 1 <= number <= 7:
            elevator1.set_storey(storey[number])
            messagebox.showinfo("Number Entered", f"You entered: {number}")
        else:
            messagebox.showerror("Invalid Input", "Please enter a number between 1 and 7")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number")

def start_tkinter():
    root = tk.Tk()
    root.title("Number Entry")

    instruction_label = tk.Label(root, text="Please enter a number (1-7):")
    instruction_label.pack(padx=20, pady=10)

    global number_entry
    number_entry = tk.Entry(root)
    number_entry.pack(padx=20, pady=10)

    submit_button = tk.Button(root, text="Submit", command=submit_number)
    submit_button.pack(padx=20, pady=10)

    root.mainloop()

def start_pygame():
    running = True
    while running:
        elevator1_targets = input_data["state"]["lifts"][0]["targets"]
        elevator2_targets = input_data["state"]["lifts"][1]["targets"]
        elevator3_targets = input_data["state"]["lifts"][2]["targets"]
        
        if elevator1_targets and not elevator1.animation_playing and not elevator1.close_doors:
            elevator1.set_storey(storey[elevator1_targets[0]])
        if elevator2_targets and not elevator2.animation_playing and not elevator2.close_doors:
            elevator2.set_storey(storey[elevator2_targets[0]])
        if elevator3_targets and not elevator3.animation_playing and not elevator3.close_doors:
            elevator3.set_storey(storey[elevator3_targets[0]])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the elevators
        all_elevators.update()
     
        for elevator in all_elevators:
            if elevator.is_at_target:
                if not elevator.animation_played:
                    elevator.play_animation_open_door()
                elif elevator.close_doors:
                    elevator.play_animation_close_door()
                    if elevator.doors_closed:
                        if elevator == elevator1 and elevator1_targets:
                            elevator1_targets.pop(0)
                            if elevator1_targets:
                                elevator1.set_storey(storey[elevator1_targets[0]])
                        if elevator == elevator2 and elevator2_targets:
                            elevator2_targets.pop(0)
                            if elevator2_targets:
                                elevator2.set_storey(storey[elevator2_targets[0]])
                        if elevator == elevator3 and elevator3_targets:
                            elevator3_targets.pop(0)
                            if elevator3_targets:
                                elevator3.set_storey(storey[elevator3_targets[0]])

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        all_elevators.draw(screen)
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()

# Run Tkinter in a separate thread
tk_thread = threading.Thread(target=start_tkinter)
tk_thread.start()

# Run Pygame in the main thread
start_pygame()
