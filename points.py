# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 10:58:11 2023

@author: userid
"""

import pygame
import sys
import random
import math

pygame.init()

screen_length=400
screen_width=300
screen=pygame.display.set_mode((screen_length,screen_width))
pygame.display.set_caption('point connection')
clock = pygame.time.Clock()

class Point(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.color=(100,100,100)
        r=2
        self.image=pygame.Surface((2*r,2*r),pygame.SRCALPHA)
        pygame.draw.circle(self.image,self.color,(r,r),r)
        self.rect=self.image.get_rect(topleft=(random.randint(0, screen_length),random.randint(0, screen_width)))
        self.dir=random.randint(0, 360)
        self.speed=1
        
    def draw(self):
        screen.blit(self.image, self.rect)
        
    def update(self):
        if self.rect.x<0:
            self.rect.x=screen_length
        if self.rect.x>screen_length:
            self.rect.x=0
        if self.rect.y<0:
            self.rect.y=screen_width
        if self.rect.y>screen_width:
            self.rect.y=0
        self.rect.x+=math.cos(self.dir)*self.speed
        self.rect.y+=math.sin(self.dir)*self.speed

class Mouse_Point(Point):
    def __init__(self):
        super().__init__()
        
    def update(self):
        mx,my=pygame.mouse.get_pos()
        self.rect.x,self.rect.y=mx,my
    
class Points_Group:
    def __init__(self,points_num):
        self.dis_max=100
        self.bri_max=220
        self.bri_min=100
        self.points=pygame.sprite.Group()
        for _ in range(points_num):
            self.points.add(Point())
        self.points.add(Mouse_Point())
            
    def draw(self):            
        points_pos=[(p.rect.x, p.rect.y) for p in self.points]
        for point_rect in points_pos:
            for rect in points_pos:
                distance=math.sqrt((point_rect[0]-rect[0])**2+(point_rect[1]-rect[1])**2)
                if distance<=self.dis_max:
                    bri=int((self.bri_max-self.bri_min)/self.dis_max*distance+self.bri_min)
                    pygame.draw.line(screen, (bri,bri,bri), point_rect, rect)
        for point in self.points:
            point.draw()
        
    def update(self):
        self.points.update()

points=Points_Group(20)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    mouse_x,mouse_y=pygame.mouse.get_pos()
    points.update()
    screen.fill((220,220,220))
    points.draw()
    
    pygame.display.flip()
    clock.tick(30)
