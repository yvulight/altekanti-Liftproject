import pygame
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading
import os
from Algorithm_v2 import run_algorithm

# Load input data
with open("algo_output.json") as f:
    input_data = json.load(f)
#load output data
with open("Input.json") as I:
    output_data = json.load(I)

# Setting Up Pygame
pygame.init()
width, height = 400, 600
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
#load background
background_path = os.path.join("images", "Elevator_background.png")
background = pygame.image.load('images/Elevator_Background.png')

# Creating Elevator Class 
class Elevator(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_y):
        #inherit from pygame.sprite.Sprites
        super(Elevator, self).__init__()
        #load image and convert it
        image_path = os.path.join("images", "elevator", "Elevator_Doors_1.png")
        self.image = pygame.image.load('images/elevator/Elevator_Doors_1.png').convert()
        self.image.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.speed_y = speed_y
        self.target_y = y
        self.people = 0
        #initiate variables for animation controlling and elevator state
        self.is_at_target = False
        #is an animation playing?
        self.animation_playing = False
        #has an animation been played at this position
        self.animation_played = False
        #should the close_doors animation be played
        self.close_doors = False
        #have the doors been closed?
        self.doors_closed = False
        
        self.position = int(7-(self.rect.y -22)/70)
        #load animation 
        self.animation_frames = [
            pygame.image.load('images/elevator/Elevator_Doors_2.png').convert() for i in range(1, 14)
        ]
        #convert every frame
        for frame in self.animation_frames:
            frame.set_colorkey((0, 0, 0), pygame.RLEACCEL)
            #
        self.anim_index = 0
    
    def update(self):
        #movement of the elevator at max target_y px per frame towards target_y
        if self.rect.y < self.target_y:
            self.rect.y += min(self.speed_y, self.target_y - self.rect.y)
        elif self.rect.y > self.target_y:
            self.rect.y -= min(self.speed_y, self.rect.y - self.target_y)
        if self.rect.y == self.target_y:
            #initiate animation 
            self.is_at_target = True
            if not self.animation_playing and not self.animation_played:
                self.animation_playing = True
                self.anim_index = 0
        else:
            #cancel animation
            self.is_at_target = False
            self.animation_playing = False
            self.animation_played = False
            self.close_doors = False
    #set a target storey 
    def set_storey(self, target_y):
        self.target_y = target_y
        #for animation control
        self.is_at_target = False
        self.animation_playing = False
        self.animation_played = False
        self.close_doors = False

    def play_animation_open_door(self):
        #if at target and animation playing proceed
        if self.is_at_target and self.animation_playing:
            #go through all the frames and display them
            if self.anim_index < len(self.animation_frames) - 1:
                self.anim_index += 1
                self.image = self.animation_frames[self.anim_index]
            else:
                #end animation on the last frame and set variables accordingly
                self.animation_played = True
                self.image = self.animation_frames[-1]
                self.close_doors = True
                self.doors_closed = False

    def play_animation_close_door(self):
        #if conditions are met play animation
        if self.is_at_target and self.close_doors:
            #go though same animation but backwards
            if self.anim_index > 0:
                self.anim_index -= 1
                self.image = self.animation_frames[self.anim_index]
            else:
                #stay on first image and set the elevator state accordingly
                self.image = self.animation_frames[0]
                self.doors_closed = True

# Create elevators and group them
all_elevators = pygame.sprite.Group()
elevator1 = Elevator(100, storey[1], 2)
elevator2 = Elevator(184, storey[2], 2)
elevator3 = Elevator(268, storey[3], 2)
all_elevators.add(elevator1, elevator2, elevator3)

# Tkinter Part
def submit_number():
    try:
        number = int(number_entry.get())
        if 1 <= number <= 7:
            elevator1.set_storey(storey[number])
            messagebox.showinfo("Number Entered", f"You entered: {number}")
            quit()
        else:
            messagebox.showerror("Invalid Input", "Please enter a number between 1 and 7")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number")

def internal_input(lift,storey):
    #print(lift,storey)
    output_data['input']['is_internal'] = True
    output_data['input']['internal']['storey'] = int(storey)
    output_data['input']['internal']['lift'] = int(lift)- 1
    send_to_algo(True)

def external_input(storey,direction_upwards):
    #print(direction_upwards,storey)
    output_data['input']['is_internal'] = False
    output_data['input']['external']['storey'] = int(storey)
    output_data['input']['external']['upwards'] = bool(direction_upwards)
    send_to_algo(False)

def send_to_algo(is_internal):
    update_output()
    with open('Input.json', 'w', encoding='utf-8') as v:
        json.dump(output_data, v, ensure_ascii=False, indent=4)
    run_algorithm

def change_direction(bool):
    global direction_upwards
    direction_upwards = bool

def start_tkinter():
    root = tk.Tk()
    #root.geometry('600x400')
    root.title("Input")

    root.resizable(0,0)
    root.columnconfigure(0, weight=2)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=2)
    root.columnconfigure(3, weight=1)

    instruction_label = tk.Label(root, text="Give an Input",font=("Helvetica", 20))
    instruction_label.grid(row=0,columnspan=4, sticky=tk.EW, padx=30, pady=10)

    Storey_list = range(1,8)
    lift_list = range(1,4)

    #Internal
    internal_label = tk.Label(root, text='Internal',font=("Helvetica", 14))
    internal_label.grid(column=0,row=1,columnspan=2,sticky=tk.EW, padx=30, pady=10)

    #lift Intern
    lift_intern_label = tk.Label(root, text='which Lift?')
    lift_intern_label.grid(column=0,row=2,padx=10, pady=10)

    lift_internal_drop = tk.StringVar(root)
    lift_internal_drop.set(lift_list[0])

    option_lift_intern = tk.OptionMenu(root, lift_internal_drop, *lift_list)
    option_lift_intern.grid(column=1,row=2, padx=10, pady=10)

    #storey intern
    storey_intern_label = tk.Label(root, text='which Storey?')
    storey_intern_label.grid(column=0,row=3,padx=10, pady=10)

    Storey_internal_drop = tk.StringVar(root)
    Storey_internal_drop.set(Storey_list[0])

    option_storey_intern = tk.OptionMenu(root, Storey_internal_drop, *Storey_list)
    option_storey_intern.grid(column=1,row=3, padx=20, pady=10)

    #intern submit
    internal_button = tk.Button(root, text="submit Internal", command=lambda: internal_input(lift_internal_drop.get(),Storey_internal_drop.get()))
    internal_button.grid(column=0, row=5, padx=20, pady=10)



    #Extern
    extern_label = tk.Label(root, text='Extern',font=("Helvetica", 14))
    extern_label.grid(column=2,row=1,columnspan=2,sticky=tk.EW, padx=30, pady=10)

    #storey intern
    storey_extern_label = tk.Label(root, text='which Storey?')
    storey_extern_label.grid(column=2,row=2,padx=10, pady=10)

    Storey_extern_drop = tk.StringVar(root)
    Storey_extern_drop.set(Storey_list[0])

    option_storey_extern = tk.OptionMenu(root, Storey_extern_drop, *Storey_list)
    option_storey_extern.grid(column=3,row=2, padx=20, pady=10)

    #direction
    direction_label = tk.Label(root, text='Direction')
    direction_label.grid(column=2,row=3, padx=30, pady=10)

    direction_up = tk.Button(root, text='Up', command= lambda:change_direction(True))
    direction_up.grid(column=3, row=3, padx=0, pady=0)

    direction_down = tk.Button(root, text='Down', command= lambda:change_direction(False))
    direction_down.grid(column=3, row=4, padx=0, pady=0)

    #intern submit
    extern_button = tk.Button(root, text="submit external", command=lambda: external_input(Storey_extern_drop.get(),direction_upwards))
    extern_button.grid(column=2, row=5, padx=20, pady=10)


    root.mainloop()

def update_output():
    #Targets
    output_data["state"]["lifts"][0]["targets"] = elevator1_targets
    output_data["state"]["lifts"][1]["targets"] = elevator2_targets
    output_data["state"]["lifts"][2]["targets"] = elevator3_targets

    output_data["state"]["lifts"][0]["position"] = elevator1.position
    output_data["state"]["lifts"][1]["position"] = elevator2.position
    output_data["state"]["lifts"][2]["position"] = elevator3.position

    



def start_pygame():
    running = True
    while running:
        global elevator1_targets
        global elevator2_targets
        global elevator3_targets
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
