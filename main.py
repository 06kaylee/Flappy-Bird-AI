import pygame
import neat
import time
import os
import random
from bird import Bird
from pipe import Pipe
from base import Base
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800
STAT_FONT = pygame.font.SysFont("comicsans", 50)
GEN = 0


BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "background.png")))


def draw_window(win, birds, pipes, base, score, gen):
    # draws background image starting at top left corner of screen
    win.blit(BACKGROUND_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    base.draw(win)
    for bird in birds:
        # draw bird over background
        bird.draw(win)

    #refresh display
    pygame.display.update()


def main(genomes, config):
    global GEN
    GEN += 1
    networks = []
    genomes_list = []
    birds = []
    

    for genome_id, genome in genomes:
        # set up an initial fitness of 0 for each genome (bird)
        genome.fitness = 0
        # set up neural network for genome
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(net)
        birds.append(Bird(230, 350))
        genomes_list.append(genome)


    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    run = True
    clock = pygame.time.Clock()
    score = 0

    while run:
        # 30 ticks every second
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # look at the first pipe in the pipe list
        pipe_index = 0
        if len(birds) > 0:
            # if the bird passed the first pipe in the list, look at the second pipe in the list
            if len(pipes) > 1 and birds[0].x_pos > pipes[0].x_pos + pipes[0].PIPE_TOP.get_width():
                pipe_index = 1
        else:
            run = False
            break

        for bird_index, bird in enumerate(birds):
            bird.move()
            genomes_list[bird_index].fitness += 0.1
            output = networks[bird_index].activate((bird.y_pos, abs(bird.y_pos - pipes[pipe_index].height), abs(bird.y_pos - pipes[pipe_index].bottom)))
            if output[0] > 0.5:
                bird.jump()


        remove_pipes = []
        add_pipe = False

        for pipe in pipes:
            for bird_index, bird in enumerate(birds):
                if pipe.collide(bird):
                    # subtract fitness from birds that possibly make it far but collide with the pipe
                    genomes_list[bird_index].fitness -= 1
                    # remove that bird from the lists
                    birds.pop(bird_index)
                    networks.pop(bird_index)
                    genomes_list.pop(bird_index)
                
                # if the bird has passed the pipe, change the bird passed variable to true and add the next pipe
                if not pipe.bird_passed and pipe.x_pos < bird.x_pos:
                    pipe.bird_passed = True
                    add_pipe = True

            # if the pipe is off the screen, add the pipe to the remove list
            if pipe.x_pos + pipe.PIPE_TOP.get_width() < 0:
                remove_pipes.append(pipe)

            pipe.move()
        
        # once the bird has passed the pipe, add to score and set up next set of pipes
        if add_pipe:
            score += 1
            #if the bird makes it through the pipe, add to fitness to encourage it to want to go through the pipe
            for genome in genomes_list:
                genome.fitness += 5
            pipes.append(Pipe(600))

        # remove the pipes in the remove list from the pipes list
        for pipe in remove_pipes:
            pipes.remove(pipe)

        # if the bird hits the floor
        for bird_index, bird in enumerate(birds):
            if bird.y_pos + bird.img.get_height() >= 730 or bird.y_pos < 0:
                birds.pop(bird_index)
                networks.pop(bird_index)
                genomes_list.pop(bird_index)

        # once bird gets good enough, break out of loop
        if score > 50:
            break

        base.move()
        draw_window(win, birds, pipes, base, score, GEN)
                
    

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    winner = population.run(main,50)
    print(f"Winner: {winner}")


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)