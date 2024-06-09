import pygame
import json

f = open("input.json")
input = json.load(f)
# Setting Up Pygame
pygame.init()
#set aspect ratio
width, height = 400, 500
screen = pygame.display.set_mode((width, height))
#name the window
pygame.display.set_caption("Elevator Sim 2024")

# For FPS and Frame Capping
clock = pygame.time.Clock()
#translate the storey into the y-coordinates
storey = {
    1: 442,
    2: 372,
    3: 302,
    4: 232, 
    5: 162,
    6: 92, 
    7: 22
}
background = pygame.image.load("images\Elevator_background.png")

# creating Elevator Class 
class Elevator(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_y):
        #inherit from sprite.Sprite 
        super(Elevator, self).__init__()
        #import main image 
        image_path = r"images\elevator\Elevator_Doors_1.png"
        self.image = pygame.image.load(image_path).convert()
        self.image.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        #speed of Elevator px per frame
        self.speed_y = speed_y

        self.target_y = y
        #variables for the elevator states
        self.is_at_target = False
        self.animation_playing = False
        self.animation_played = False
        self.close_doors = False
        self.doors_closed = False

        #load animation frames 
        self.animation_frames = [
            pygame.image.load(f"images\elevator\elevator_doors_{i}.png").convert() for i in range(1, 14)
        ]
        for frame in self.animation_frames:
            frame.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.anim_index = 0

    def update(self):
        # move towards target_y, at a max pace of speed_y
        if self.rect.y < self.target_y:
            self.rect.y += min(self.speed_y, self.target_y - self.rect.y)
        elif self.rect.y > self.target_y:
            self.rect.y -= min(self.speed_y, self.rect.y - self.target_y)
        #check if elevator at target storey
        if self.rect.y == self.target_y:
            self.is_at_target = True
            # initiate animation
            if not self.animation_playing and not self.animation_played:
                self.animation_playing = True
                self.anim_index = 0
            #update state of the elevator for animations
        else:
            self.is_at_target = False
            self.animation_playing = False
            self.animation_played = False
            self.close_doors = False
    #set the target_y and update state
    def set_storey(self, target_y):
        self.target_y = target_y
        self.is_at_target = False
        self.animation_playing = False
        self.animation_played = False
        self.close_doors = False
    # animation to open the door 
    def play_animation_open_door(self):
        if self.is_at_target and self.animation_playing:
            if self.anim_index < len(self.animation_frames) - 1:
                self.anim_index += 1
                self.image = self.animation_frames[self.anim_index]
            else:
                self.animation_played = True
                self.image = self.animation_frames[-1]
                self.close_doors = True
                elevator.doors_closed = False
    # animation to close the door (same frames but in reverse)
    def play_animation_close_door(self):
        if self.is_at_target and self.close_doors:
            if self.anim_index > 0:
                self.anim_index -= 1
                self.image = self.animation_frames[self.anim_index]
            else:
                self.image = self.animation_frames[0]
                elevator.doors_closed = True

all_elevators = pygame.sprite.Group()
#create 3 instances of the elevator at defined coordinates and speed
elevator1 = Elevator(100, storey[1], 5)
elevator2 = Elevator(184, storey[2], 5)
elevator3 = Elevator(268, storey[3], 5)
#group all instances
all_elevators.add(elevator1)
all_elevators.add(elevator2)
all_elevators.add(elevator3)

# Main game loop
running = True
while running:

    #creating lists with the targets for every elevator
    elevator1_targets = input["state"]["lifts"][0]["targets"]
    elevator2_targets = input["state"]["lifts"][1]["targets"]
    elevator3_targets = input["state"]["lifts"][2]["targets"]
    #update the target y for each elevator in case there is no animation playing and there are still other targets
    if len(elevator1_targets) > 0 and not elevator1.animation_playing and not elevator1.close_doors:
        elevator1.set_storey(storey[elevator1_targets[0]])
        print("elevator1:", elevator1_targets)
    if len(elevator2_targets) > 0 and not elevator2.animation_playing and not elevator2.close_doors:
        elevator2.set_storey(storey[elevator2_targets[0]])
        #print("elevator2:", elevator2_targets)
    if len(elevator3_targets) > 0 and not elevator3.animation_playing and not elevator3.close_doors:
        elevator3.set_storey(storey[elevator3_targets[0]])
        #print("elevator3:", elevator3_targets)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Update the elevators
    all_elevators.update()
 
    for elevator in all_elevators:
        if elevator.is_at_target:
            #play the open doors animation
            if not elevator.animation_played:
                elevator.play_animation_open_door()
            #play the close doors animation
            elif elevator.close_doors:
                elevator.play_animation_close_door()
                # update the target y for each elevator if the animations have finished and there are other target y 
                if elevator == elevator1 and len(elevator1_targets) > 0 and elevator.doors_closed:
                    elevator1_targets.pop(0)
                    if len(elevator1_targets) > 0:
                        elevator1.set_storey(storey[elevator1_targets[0]])
                if elevator == elevator2 and len(elevator2_targets) > 0 and elevator.doors_closed:
                    elevator2_targets.pop(0)
                    if len(elevator2_targets) > 0:
                        elevator2.set_storey(storey[elevator2_targets[0]])
                if elevator == elevator3 and len(elevator3_targets) > 0 and elevator.doors_closed:
                    elevator3_targets.pop(0)
                    if len(elevator3_targets) > 0:
                        elevator3.set_storey(storey[elevator3_targets[0]])

    
    screen.fill((0, 0, 0))

    #draw background
    screen.blit(background, (0, 0))
    all_elevators.draw(screen)

    pygame.display.flip()

    # Frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()