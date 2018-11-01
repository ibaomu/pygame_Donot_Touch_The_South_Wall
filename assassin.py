# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 13:52:48 2018

@author: 某树
"""

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """己方飞船的类"""    
    def __init__(self,ai_settings,screen):#用了sb则建立实例要在ship前面
        """初始化飞船并设置其初始位置"""
        super().__init__()        
        self.screen = screen

        #加载飞船的图像并获取其外接矩形
        self.image = pygame.image.load('images/qiui.png')        
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        
        #将每艘新飞船放在南墙顶部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom       
        #移动标志
        self.moving_right = False
        self.moving_left = False        
        
    def update(self):
        """根据移动标志调整飞船位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.rect.centerx -= self.ai_settings.ship_speed_factor
            
    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)
    
    def center_ship(self):
        """让飞船在屏幕底端居中"""
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom