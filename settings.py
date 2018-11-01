# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 13:40:45 2018

@author: 某树
"""
import ctypes

class Settings():
    """存储《别碰南墙》的所有设置的类"""
    def __init__(self):
        """初始化游戏的静态设置"""
        #屏幕设置
        self.screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        self.screen_height = ctypes.windll.user32.GetSystemMetrics(1) - 59
        self.bg_color = (242,167,220)#根据对象颜色设置背景色。可以抠图吧
        self.ship_limit = 3
        #子弹设置
        self.bullet_width = 399
        self.bullet_height = 13
        self.bullet_color = 60,60,60 #啥颜色？
        self.bullet_allowed = 4
       #刺客设置
        self.fleet_drop_speed = 30
    #加快游戏节奏的速度
        self.speedup_scale = 1.05
        #敌人点数提高的速度
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.alien_speed_factor = 1
        self.bullet_speed_factor = 3
        #fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1
        #计分
        self.alien_points = 5
        
    def increase_speed(self):
        """提高速度设置和敌人点数"""
        self.ship_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)        