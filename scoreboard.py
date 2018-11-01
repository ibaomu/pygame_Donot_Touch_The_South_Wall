# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 20:21:27 2018

@author: 某树
"""

import pygame.font
from pygame.sprite import Group
from assassin import Ship

class Scoreboard():
    """显示得分信息"""
    def __init__(self,ai_settings,screen,stats):
        """初始化显示得分所涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        
        
        #加载南墙的图像并获取其外接矩形
        self.wall_image = pygame.image.load('images/wall.png')        
        self.wall_rect = self.wall_image.get_rect()
        
        #将南墙放在屏幕底部
        self.wall_rect.centerx = self.screen_rect.centerx
        self.wall_rect.bottom = self.screen_rect.bottom 
        
        
        
        
        
        
        #显示得分信息时使用的字体设置
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont("kaiti",19)
        
        #准备包含最高得分、当前得分、等级以及南墙的图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_wall()
        
    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        rounded_score = round(self.stats.score,-1)
        score_str = "颜值：{:,}".format(rounded_score)
        #score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str,True,self.text_color,
                                            self.ai_settings.bg_color)
        
        #将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top =20
    
    def prep_high_score(self):
        """将最高得分转换为渲染的图像"""
        high_score = round(self.stats.high_score,-1)
        high_score_str = "历史最高颜值:{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str,
            True,self.text_color,self.ai_settings.bg_color)
            
        #将最高分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
        
    def show_score(self):
        """在屏幕上显示等级和得分"""
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        #绘制飞船        
        self.ships.draw(self.screen)
    def prep_level(self):
        """将等级渲染为图像"""
        self.level_image = self.font.render(("颜值等级："+str(self.stats.level)),
                            True,self.text_color,self.ai_settings.bg_color)
        #将等级放在得分的下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
    
    def prep_ships(self):
        """显示还余下多少飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings,self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
    def prep_wall(self):
        """在指定位置绘制南墙"""
        self.screen.blit(self.wall_image,self.wall_rect)
        