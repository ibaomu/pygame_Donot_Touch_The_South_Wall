# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 13:01:10 2018

@author: 某树
"""
     
import pygame
import game_functions as gf

from boss import Boss
from scoreboard import Scoreboard
from button import Button
from game_stats import GameStats
from pygame.sprite import Group
from settings import Settings
from assassin import Ship


#获取玩家电脑屏幕尺寸！！！

msg = """操作提示：按空格键攻击，‘←’和‘→’键控制人物方向，‘esc’键退出游戏"""

def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    #pygame.mixer.init()
    font1 = pygame.font.SysFont("kaiti",24)
    imgText = font1.render(msg,True,(0,0,0))
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height),pygame.RESIZABLE)
        #窗口标题
    pygame.display.set_caption("别撞南墙")
    
    #创建存储游戏统计信息的实力，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)
    #创舰一艘飞船、一个子弹编组、一个外星人编组
    bullets = Group()
    ship = Ship(ai_settings,screen)
    boss = Boss(ai_settings,screen)
    aliens = Group()
    #创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)
    
    #sound = pygame.mixer.Sound('C:/LOP/python_work/donot_touch_the_south_wall/music/bgm.ogg')
    #创建play按钮
    play_button = Button(ai_settings,screen,"开始游戏")    
    #开始游戏的主循环
    while True:
        
        gf.check_events(ai_settings,screen,ship,bullets,
                        stats,play_button,aliens,sb)
        #sound.play()
        if stats.game_active:
            
            ship.update()
            gf.update_bullets(bullets,aliens,ai_settings,screen,ship,stats,sb,boss)
            gf.update_aliens(aliens,ai_settings,ship,screen,bullets,stats,sb,boss)
            gf.update_boss(boss,screen,stats,aliens,ai_settings,ship,bullets,sb)
        gf.update_screen(ai_settings,screen,ship,bullets,aliens,
                         stats,play_button,sb,boss,imgText)
        #sound.stop
        
run_game()
    