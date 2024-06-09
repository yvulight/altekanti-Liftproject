import pygame
import json

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
        #set speed of Elevator px per frame
        self.speed_y = speed_y
        #set target y, e.g. target storey
        self.target_y = y
        #for animations to be played correctly
        self.is_at_target = False
        self.animation_playing = False
        self.animation_played = False
        self.close_doors = False
        #load animation
        self.animation_frames = [
            pygame.image.load(f"images\elevator\elevator_doors_{i}.png").convert() for i in range(1, 14)
        ]
        for frame in self.animation_frames:
            frame.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        #order of the animation sprites
        self.anim_index = 0

    def update(self):
        # move towards target_y
        if self.rect.y < self.target_y:
            self.rect.y += min(self.speed_y, self.target_y - self.rect.y)
        elif self.rect.y > self.target_y:
            self.rect.y -= min(self.speed_y, self.rect.y - self.target_y)
        # 
        if self.rect.y == self.target_y:
            self.is_at_target = True
            # initiate animation
            if not self.animation_playing and not self.animation_played:
                self.animation_playing = True
                self.anim_index = 0
            #
        else:
            self.is_at_target = False
            self.animation_playing = False
            self.animation_played = False
            self.close_doors = False
    # function to set the target_y 
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
    # animation to close the door 
    def play_animation_close_door(self):
        if self.is_at_target and self.close_doors:
            if self.anim_index > 0:
                self.anim_index -= 1
                self.image = self.animation_frames[self.anim_index]
            else:
                self.image = self.animation_frames[0]

all_elevators = pygame.sprite.Group()
#create elevators and group them
elevator1 = Elevator(100, storey[1], 5)
elevator2 = Elevator(184, storey[2], 5)
elevator3 = Elevator(268, storey[3], 5)
all_elevators.add(elevator1)
all_elevators.add(elevator2)
all_elevators.add(elevator3)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #for testing purposes
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                elevator1.set_storey(storey[1])
                elevator2.set_storey(storey[3])
                elevator3.set_storey(storey[2])
            elif event.key == pygame.K_2:
                elevator1.set_storey(storey[2])
                elevator3.set_storey(storey[3])
                elevator2.set_storey(storey[1])

    # Update the elevators
    all_elevators.update()

    for elevator in all_elevators:
        if elevator.is_at_target:
            if not elevator.animation_played:
                elevator.play_animation_open_door()
            elif elevator.close_doors:
                elevator.play_animation_close_door()

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    all_elevators.draw(screen)

    pygame.display.flip()

    # Frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()