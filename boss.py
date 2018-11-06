# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 17:35:48 2018

@author: 某树
"""

import pygame
from pygame.sprite import Sprite
from random import choice
class Boss(Sprite):
    """Boss及其掉落品的类"""    
    def __init__(self,ai_settings,screen):
        """初始化飞船并设置其初始位置"""
        super().__init__() 
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        #加载高富帅敌人,并设置其位置
        self.iamge = pygame.image.load('images/sp.png')
        self.rect = self.iamge.get_rect()
        self.rect.x = self.ai_settings.screen_width / 2
        self.rect.y = 30
        #随机抽取高富帅每次漫步的X，Y的方向和距离
        #正向朝下的数值大于反向，使其总体趋势是朝下的
        self.x_direction = choice([2,-1.6])
        self.x_distance = choice([1,1.5,2,2.5])
        self.y_direction = choice([1,-1])
        self.y_distance = choice([1,1.5,2,2.5])
        
    def blit_boss(self):
        """在指定位置绘制高富帅"""
        self.screen.blit(self.iamge,self.rect)
    
    def random_walk(self):
        """高富帅随机漫步"""
        self.rect.x += self.x_direction * self.x_distance        
        self.rect.y += self.y_direction * self.y_distance
            
    def check_edges(self):
        """如果高富帅位于屏幕边缘，方向折返"""
        if self.rect.right >= self.screen_rect.right:
            self.x_direction *= -1
        elif self.rect.left <= 0:
            self.x_direction *= -1
        elif self.rect.top <= 0:
            self.y_direction *= -1
    def boss_again(self):
        self.rect.x = self.ai_settings.screen_width / 2
        self.rect.y = 30