import pygame
import neat
import random
from Fp_class import bird



def evalution(genomes,config):
    
    
    points = 0
    entities = []   # don't know
    gen = []        # stores fitness from generations
    birdies = []    # birds class stores

    floor = pygame.Rect(0,580,800,20)
    screen = pygame.display.set_mode((500,600))
    clock = pygame.time.Clock()
    run = 1
    
    pp_s = 60
    spacing = 100
    new_height = random.randint(5,400)
    
    font = pygame.font.SysFont("arial", 30)
    pipes = {"upper1":pygame.Rect(600,0,pp_s,new_height), "lower1":pygame.Rect(600,new_height+spacing,pp_s,600-new_height-spacing),
            "nupper":pygame.Rect(600,0,pp_s,300), "nlower":pygame.Rect(600,450,pp_s,300)}

    for i, g in genomes:
        ent = neat.nn.FeedForwardNetwork.create(g, config)
        entities.append(ent)
        g.fitness = 0
        gen.append(g)
        birdies.append(bird(screen))

    while run and len(birdies)>0:
        clock.tick(120)
        screen.fill("lightblue")

        
        
        pygame.draw.rect(screen,"green",pipes["upper1"])
        pygame.draw.rect(screen,"green",pipes["lower1"])
        pygame.draw.rect(screen,"red",floor)
           
        keys = pygame.key.get_pressed()

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                print("EXIT")
                run = 0
        
        if keys[pygame.K_ESCAPE]:
            run = 0
            pygame.QUIT

        pipes["upper1"].move_ip(-2,0)
        pipes["lower1"].move_ip(-2,0)


        if pipes["upper1"].move(0,0)[0] <= 0-pp_s:
            new_height = random.randint(5,400)
            
            pipes["nupper"] = pygame.Rect(600,0,pp_s,new_height)
            pipes["nlower"] = pygame.Rect(600,new_height+spacing,pp_s,600-new_height-spacing)
            pipes["lower1"] = pipes["nlower"].copy()
            pipes["upper1"] = pipes["nupper"].copy()
            
            
        
        if pipes["upper1"].move(0,0)[0] == (screen.get_width()/2)-pp_s:
            points+=1

        
        for x, b in enumerate(birdies):
            gen[x].fitness += 0.1
            b.draw_bird(screen)
            b.grav()
            b.collide(pipes,floor)
           
           
            # output based on receving 2 inputs
            output = entities[x].activate((b.birdo.move(0,0)[1]-pipes["lower1"][1], b.birdo.move(0,0)[1]-pipes["upper1"][3]))
            
            finalOP = output.index(max(output)) - 1
            
            birdies[x].jumper_neat(finalOP)
            
            if b.collide(pipes,floor):
                gen[x].fitness -= 5
                gen[x].fitness += points
                entities.pop(x)
                gen.pop(x)
                birdies.pop(x)
				
			# if ge[x].fitness >= 10000:
				# 	print("SCORE -> {}".format(balls[x].score))
				# 	run = False
				# 	break         
            ######'''
        if len(birdies) == 0:
            run = False
            break
        
        
        numbers =  font.render(str(points),True,"black")
        n_alive = font.render("Alive:"+str(len(birdies)),True,"black")
        screen.blit(numbers,(240,10))
        screen.blit(n_alive,(40,10))
        pygame.display.flip()       # mostra o que ocorre no ecrã
    print(points)
    


def run_neat(conf):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         conf)
    population = neat.Population(config)
    
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(5))
    winner = population.run(evalution,20)

    print("Best fitness -> {}".format(winner))


pygame.init()

pygame.display.set_caption("Fp")

if __name__ == "__main__":
      run_neat("config_file.ini")

