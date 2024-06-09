import pygame
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading
import os
import math


def sort_list(input,lift_number):
    lift_position = input['state']['lifts'][lift_number]['position'] # lift position zb. 1
    lift_targets = input['state']['lifts'][lift_number]['targets'] #Liste mit den momentanen targets zb. [5,6,7]
    all_list = [lift_position]+lift_targets

    if input['input']['is_internal']:
        new_target = input['input']['internal']['storey']
        direction_upwards = lift_position <= new_target
    else:
        direction_upwards = input['input']['external']['upwards']
        new_target = input['input']['external']['storey']

    done = False
    #Alles durchgehen und checken ob dazwischen mit beruecksichtigung von direction
    if direction_upwards: # hochfahren
        for i in range(1,len(all_list)):
                if all_list[i-1] <= new_target < all_list[i]:
                    all_list.insert(i, new_target)
                    done = True
                    break
    if not direction_upwards: # runterfahren
        for i in range(1,len(all_list)):
                if all_list[i-1] >= new_target > all_list[i]:
                    all_list.insert(i, new_target)
                    done = True
                    break
    if not done:
        all_list.append(new_target)

    all_list.pop(0)
    return all_list


def choose_lift(input):
    #INPUT IN VARIABELN SPEICHERN
    #inputs
    where_pressed = input['input']['external']['storey']
    direction_upwards = input['input']['external']['upwards']

    #die drei state-listen
    lift_positions_list = []
    lift_targets_list = []
    lift_people_list = []
    for i in range(3):
        lift_positions_list.append(input['state']['lifts'][i]['position'])
        lift_targets_list.append(input['state']['lifts'][i]['targets'])
        lift_people_list.append(input['state']['lifts'][i]['people'])

    # Überprüfe, ob ein Lift bereits an der gleichen Position ist
    for lift_number in range(3):
        if lift_positions_list[lift_number] == where_pressed and direction_upwards == (lift_positions_list[lift_number] < where_pressed) and lift_people_list[lift_number] < 10:
            return lift_number, where_pressed in lift_targets_list[lift_number]

    goodness_list = []
    for lift_number in range(3):
        if lift_people_list[lift_number] >= 14:
            goodness_list.append(float('inf'))  # Dieser Lift kann keine neuen externen Ziele annehmen
            continue

        value = abs(lift_positions_list[lift_number] - where_pressed)
        same_direction = (lift_positions_list[lift_number] < where_pressed) == direction_upwards
        value += 0.7 * same_direction  # Werte die Fahrtrichtung höher
        value += 0.8 * abs(same_direction - 1)  # Verringere den Wert, wenn die Fahrtrichtung unterschiedlich ist

        if where_pressed in lift_targets_list[lift_number]:
            target_index = lift_targets_list[lift_number].index(where_pressed)
        else:
            target_index = len(lift_targets_list[lift_number])

        value += 1.2 * (target_index + 1)
        someone_enters = 1 if lift_positions_list[lift_number] == where_pressed else 0
        value += 5 * someone_enters
        goodness_list.append(value)

    # Füge eine Überprüfung hinzu, um sicherzustellen, dass `goodness_list` immer die richtige Anzahl von Elementen hat
    while len(goodness_list) < 3:
        goodness_list.append(float('inf'))

    lift_number = goodness_list.index(min(goodness_list))
    already_in_targets = where_pressed in lift_targets_list[lift_number]
    return lift_number, already_in_targets

def run_algorithm():
    # Opening JSON file
    f = open('Input.json')

    # returns JSON object as a dictionary
    input = json.load(f)
    output = input.copy()
    max_people = 14
    where_pressed = input['input']['external']['storey']



    #Falls der Input INTERNim Lift ist, muss einfach das stockwerk der Target liste hinzugefügt werden
    if input['input']['is_internal']:
        lift_number = input['input']['internal']['lift']
        target = input['input']['internal']['storey']
        already_in_targets = False

    #Falls der Input EXTERN ist, muss heruasgefunden werden welcher Lift die Person abhohlt
    if not input['input']['is_internal']:
        lift_number, already_in_targets = choose_lift(input)
        target = input['input']['external']['storey']
        print(lift_number, already_in_targets)


    #SORT LISTS ---- SORT
    if not already_in_targets and len(input['state']['lifts'][lift_number]['targets']) > 0:
        lift_targets = sort_list(input, lift_number)
        output['state']['lifts'][lift_number]['targets'] = lift_targets
    else: #Input einfach anfuegen wenn noch kein Element in targets
        lift_targets = input['state']['lifts'][lift_number]['targets'].append(target)




    #delete Input part from Output.json
    output.pop('input')

    f.close()

    with open('algo_output.json', 'w', encoding='utf-8') as v:
        json.dump(output, v, ensure_ascii=False, indent=4)


# Load input data
with open("algo_output.json") as f:
    input_data = json.load(f)
#load output data
with open("Input.json") as I:
    output_data = json.load(I)

# Setting Up Pygame
pygame.init()
<<<<<<< HEAD
width, height = 400, 500
=======
pygame.mixer.init()
width, height = 400, 600
>>>>>>> f4d192f621ba19c1a34af7adee0110195ed59072
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Elevator Sim 2024")

# For FPS and Frame Capping
clock = pygame.time.Clock()
#background music
pygame.mixer.music.load("masterpiece.wav")
pygame.mixer.music.play(loops = -1)
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
    #messagebox.showinfo('Internal input sent to Algorithm:Storey:{storey},Lift:{lift}')
    send_to_algo(True)

def external_input(storey,direction_upwards):
    #print(direction_upwards,storey)
    output_data['input']['is_internal'] = False
    output_data['input']['external']['storey'] = int(storey)
    output_data['input']['external']['upwards'] = bool(direction_upwards)
    directions = {True: 'up', False:'down'}
    #messagebox.showinfo('External input sent to Algorithm:Storey:{1},direction:{1}'.format(storey,directions[direction_upwards]))
    send_to_algo(False)

def send_to_algo(is_internal):
    update_output()
    with open('Input.json', 'w', encoding='utf-8') as v:
        json.dump(output_data, v, ensure_ascii=False, indent=4)
    run_algorithm()
    input_changed = True

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
    global elevator1_targets
    global elevator2_targets
    global elevator3_targets
    global input_changed
    input_changed = True
    while running:
        
        if input_changed:
            with open("algo_output.json") as f:
                input_data = json.load(f)
            elevator1_targets = input_data["state"]["lifts"][0]["targets"]
            elevator2_targets = input_data["state"]["lifts"][1]["targets"]
            elevator3_targets = input_data["state"]["lifts"][2]["targets"]
            input_changed = False


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
                #play animation to open door at target
                if not elevator.animation_played:
                    elevator.play_animation_open_door()
                #play animation to close door if state is matched
                elif elevator.close_doors:
                    elevator.play_animation_close_door()
                    if elevator.doors_closed:
                        #pop the first element in the elevator_targets list so that it can move to the next target
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
