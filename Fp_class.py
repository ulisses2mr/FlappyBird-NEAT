import pygame


class bird:
    
    def __init__(self,screen):
        self.birdo = pygame.Rect(screen.get_width()/2,screen.get_height()*(1/5),20,20)
        self.birdo_b = pygame.Rect(screen.get_width()/2,screen.get_height()*(1/5),22,22)
        self.jump = 20
        self.space_up = True
        self.states={"in_jump" : False, "glide" : False, "alive":True}
        self.counter = 0
        self.floor = pygame.Rect(0,580,800,20)
        self.gravity = 4
        self.points = 0
        
        

    def draw_bird(self,screen):
        pygame.draw.rect(screen,"black",self.birdo_b)
        pygame.draw.rect(screen,"yellow",self.birdo)

    def jumper(self,keys):
        if not keys[pygame.K_SPACE]:
            self.space_up = True
        
        if keys[pygame.K_SPACE] and self.space_up:
            self.states["in_jump"] = True
            self.states["glide"] = False
            self.space_up = False

        if self.states["in_jump"]:
            self.birdo.move_ip(0,-(self.gravity+2.5))
            self.counter+=1
            if self.counter >= 2*self.jump:
                self.states["in_jump"] = False
                self.states["glide"] = True
                self.counter = 0
        
        if self.states["glide"]:
            self.counter+=1
            self.birdo.move_ip(0,-(self.gravity-1))
            if self.counter >= (self.jump/5):
                self.states["glide"] = False
    

    def jumper_neat(self,command):     
        if command:
            self.states["in_jump"] = True
            self.states["glide"] = False

        if self.states["in_jump"]:
            self.birdo.move_ip(0,-(self.gravity+2.5))
            self.birdo_b.move_ip(0,-(self.gravity+2.5))
            self.counter+=1
            if self.counter >= 2*self.jump:
                self.states["in_jump"] = False
                self.states["glide"] = True
                self.counter = 0
        
        if self.states["glide"]:
            self.counter+=1
            self.birdo.move_ip(0,-(self.gravity-1))
            self.birdo_b.move_ip(0,-(self.gravity-1))
            if self.counter >= (self.jump/5):
                self.states["glide"] = False


    def grav(self):
        self.birdo.move_ip(0,self.gravity)
        self.birdo_b.move_ip(0,self.gravity)

    def collide(self,pipes,floor):
         if self.birdo.move(0,0)[1] <= -10 or self.birdo.colliderect(pipes["lower1"]) or self.birdo.colliderect(pipes["upper1"]) or self.birdo.colliderect(floor):
            return True
