# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 20:08:44 2018

@author: 某树
"""

import pygame

class Wall():
    """加入南墙"""
    def __init__(self,screen):
        """初始化南墙的属性"""
        self.screen = screen
        #加载南墙的图像并获取其外接矩形
        self.image = pygame.image.load('images/wall.png')        
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        #将南墙放在屏幕底部
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom       
    
    def blit_wall(self,screen):
        """在指定位置绘制南墙"""
        self.screen.blit(self.image,self.rect)
        