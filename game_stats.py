# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 15:39:10 2018

@author: 某树
"""

import json

class GameStats():
    """跟踪游戏的统计信息"""
    def __init__(self,ai_settings):
        """初始化统计信息"""
        #游戏刚启动时处于非活动状态
        self.game_active = False
        self.ai_settings = ai_settings
        self.reset_stats()
        self.score = 0
        self.high_score = self.high_score_load()
    
    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level =1

    def high_score_load(self):
        filename = "high_score.json"
        with open(filename) as f_obj:
            return json.load(f_obj)