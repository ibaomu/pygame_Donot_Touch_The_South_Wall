# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 09:25:03 2018

@author: 某树
"""

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个敌人的类"""
    def __init__(self,ai_settings,screen):
        """初始化敌人并设置其的位置"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        #加载敌人图像，并设置其rect属性

        self.image = pygame.image.load('images/q;di0.png')
        self.rect = self.image.get_rect()
        
        #表示每个外星人最初都在屏幕的左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #存储每个外星人的准确位置，小数化
        self.rect.x = float(self.rect.x)
        
    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image,self.rect)
    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """向右或向左移动的外星人"""
        self.rect.x += (self.ai_settings.alien_speed_factor * 
                        self.ai_settings.fleet_direction)
     