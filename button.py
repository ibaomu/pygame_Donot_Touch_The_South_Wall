# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:38:25 2018

@author: 某树
"""

import pygame.font

class Button():
    """一个开始游戏的按钮"""
    def __init__(self,ai_settings,screen,msg):
        """初始化按钮的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        #设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (0,0,0)
        self.text_color = (255,0,0)
        self.font = pygame.font.SysFont("kaiti",48)#设置字体字号
        
        #创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center
        
        #按钮的标签只需要创建一次
        self.prep_msg(msg)
        
        #创建南墙
        #self.wall
    def prep_msg(self,msg):
        """将msg渲染为图像，并使其在按钮上居中"""
        self.msg_image = self.font.render(msg,True,self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        #创建文本图像的位置对象并存储获得的图像默认位置
        self.msg_image_rect.center = self.rect.center
        #使文本图像的位置在按钮的中间
    
    def draw_button(self):
        #创建一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)
