import pygame
import os

class Bird:
    BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", f"bird{i}.png"))) for i in range(1,4)]
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y_pos
        self.img_count = 0
        self.img = self.BIRD_IMGS[0]
    

    def jump(self):
        self.velocity = -10.5
        # tick count keeps track of when the bird last jumped
        self.tick_count = 0
        self.height = self.y_pos

    def move(self):
        self.tick_count +=1

        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count**2

        # if bird is moving down more than 16 pixels
        if displacement >= 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2

        self.y_pos = self.y_pos + displacement

        # if bird is moving up the screen
        if displacement < 0 or self.y_pos < self.height + 50:
            # tilt the bird up 25 degrees
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            # tilt the bird downwards
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.BIRD_IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.BIRD_IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.BIRD_IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.BIRD_IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.BIRD_IMGS[0]
            self.img_count = 0

        # if bird is tilted down, just show img of bird with wings flat
        if self.tilt <= -80:
            self.img = self.BIRD_IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2
    

        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        # rotates image around the center of the image instead of top left
        new_rect = rotated_img.get_rect(center = self.img.get_rect(topleft = (self.x_pos, self.y_pos)).center)
        win.blit(rotated_img, new_rect.topleft)
    

    def get_mask(self):
        return pygame.mask.from_surface(self.img)



