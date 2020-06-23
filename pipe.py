import pygame
import random
import os

class Pipe:
    GAP = 200
    VEL = 5
    PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))

    def __init__(self, x_pos):
        self.x_pos = x_pos
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(self.PIPE_IMG, False, True)
        self.PIPE_BOTTOM = self.PIPE_IMG
        self.bird_passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x_pos -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x_pos, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x_pos, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # offset is how far away the masks are from each other
        top_offset = (self.x_pos - bird.x_pos, self.top - round(bird.y_pos))
        bottom_offset = (self.x_pos - bird.x_pos, self.bottom - round(bird.y_pos))

        # returns none if the masks do not overlap eachother
        bottom_collision_point = bird_mask.overlap(bottom_mask, bottom_offset)
        top_collision_point = bird_mask.overlap(top_mask, top_offset)

        if bottom_collision_point or top_collision_point:
            return True
        return False