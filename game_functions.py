# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 14:45:36 2018

@author: 某树
"""

import sys
import pygame
import json

from time import sleep
from enemy import Alien
from weapon import Bullets


def ship_ruin(aliens,ai_settings,ship,screen,bullets,stats,sb,boss):
    """响应被敌人撞到的飞船"""
    
    if stats.ships_left > 0:
        stats.ships_left -= 1
        
        #更新记分牌的剩余生命
        sb.prep_ships()
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #暂停
        sleep(0.5)
        #创建一群新的外星人，并将飞船和高富帅重置为初始位置
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        #重置boss的位置为初始位置
        boss.rect.x = ai_settings.screen_width / 2
        boss.rect.y = 30
        
        
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
def get_number_aliens_x(ai_settings,alien_width):
    """计算每行可容纳多少敌人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2* alien_width))
    return number_aliens_x

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人并将其放在当前行上"""
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.rect.x = alien_width + 2 * alien_width *alien_number
    alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(ai_settings,ship_height,alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -
                            (5*alien_height)-ship_height)
    number_rows = int(available_space_y / (2*alien_height))
    return number_rows

def create_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""
    #创建一个外星人，并计算每行可容纳多少个外星人
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    #创建外星人群
    for row_number in range(number_rows):
        for alien_number  in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)
        
def fire_bullet(ai_settings,screen,ship,bullets):
    """如果还没有到达极限，就发射一颗子弹"""
     #创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) <= ai_settings.bullet_allowed:
        new_bullet = Bullets(ai_settings,screen,ship)
        bullets.add(new_bullet)
 
def check_keydown_events(event,ai_settings,screen,ship,bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
           
def check_keyup_events(event,ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
        
def check_events(ai_settings,screen,ship,bullets,stats,play_button,aliens,sb):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
            check_keydown_events(event,ai_settings,screen,ship,bullets)
            if event.key == pygame.K_ESCAPE:
                sys.exit()#退出
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats,play_button,mouse_x,mouse_y,aliens,bullets,
                  ai_settings,screen,ship,sb)
            #位置参数要对齐形参实参
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
def check_play_button(stats,play_button,mouse_x,mouse_y,aliens,bullets,
                      ai_settings,screen,ship,sb):
    """玩家单击play按钮时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏的动态设置
        ai_settings.initialize_dynamic_settings()        
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息        
        stats.reset_stats()       
        stats.game_active = True
        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        
def check_fleet_edges(aliens,ai_settings):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_director(ai_settings,aliens)
            break

def check_bullet_alien_cllisions(ai_settings,aliens,bullets,
                                 screen,ship,stats,sb,boss):
    """响应子弹和敌人的碰撞"""
    #精灵组碰撞，返回的字典是以第二个组的值作为项目，之前两个组位置搞反了
    #经验告诉我，千万不要随意更改参数的位置，千万要看库文档！！！
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)#对齐参数
    if collisions:
        for aliens in collisions.values():#aliens是碰撞检测中子弹碰到的所有敌人
            stats.score += ai_settings.alien_points * len(aliens)
        stats.score += ai_settings.alien_points
        sb.prep_score()
    check_high_score(stats,sb)
    #如果敌人被清空，且不是boss出场的清空，则提升游戏进度
    if  len(aliens) == 0 and stats.level % 3 != 0:
        #清空现有子弹，加快游戏节奏，并创建一群新的外星人
        bullets.empty()#清空子弹以便新一轮进攻的火力完备
        ai_settings.increase_speed()
        #提升等级,更新记分板信息
        stats.level += 1
        sb.prep_level()
        sb.prep_ships()
        create_fleet(ai_settings,screen,ship,aliens)
   
def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets,sb,boss):
    """检查是否有敌人或者boss到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞到一样进行处理
            ship_ruin(aliens,ai_settings,ship,screen,bullets,stats,sb,boss)
            break
    if boss.rect.bottom >= screen_rect.bottom:
        ship_ruin(aliens,ai_settings,ship,screen,bullets,stats,sb,boss)
        
def check_high_score(stats,sb):
    """检查是否诞生了新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score    
        sb.prep_high_score()
        #存储最高分数
        filename = "high_score.json"
        with open(filename,'w') as f_obj:
            json.dump(stats.high_score,f_obj)
        
            
def change_fleet_director(ai_settings,aliens):
    """将外星人群下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_screen(ai_settings,screen,ship,bullets,aliens,stats,
                  play_button,sb,boss):
           #每次循环时都重绘屏幕
        screen.fill(ai_settings.bg_color)
        #在飞船和外星人后面重绘所有子弹
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        ship.blitme()
        #每提升指定级数出现高富帅，小兵清空不出现
        if stats.level % 3 == 0:
            aliens.empty()
            boss.blit_boss()
        aliens.draw(screen)
        #显示得分和南墙
        sb.show_score()
        sb.prep_wall()
        #如果游戏处于非活动状态，就绘制按钮
        if not stats.game_active:
            play_button.draw_button()
            
        #让最近绘制的屏幕可见
        pygame.display.flip()
        
def update_bullets(bullets,aliens,ai_settings,screen,ship,stats,sb,boss):
    """更新子弹的位置，并删除已消失的子弹"""
    #更新子弹位置, 并删除已消失的子弹
    bullets.update()#用来更新子弹编组的位置，包括了速度
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_cllisions(ai_settings,aliens,bullets,
                                 screen,ship,stats,sb,boss)
  
def update_aliens(aliens,ai_settings,ship,screen,bullets,stats,sb,boss):
    """检查是否有外星人在屏幕边缘，并更新外星人群中所有外星人的位置"""
    check_fleet_edges(aliens,ai_settings)#对齐参数啊！
    aliens.update()
    
    #检测外星人和和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_ruin(aliens,ai_settings,ship,screen,bullets,stats,sb,boss)
    
    #检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets,sb,boss)

def update_boss(boss,screen,stats,aliens,ai_settings,ship,bullets,sb):
    """检查boss是否在屏幕边缘，并更新其位置"""
    if stats.level % 3 == 0:
        boss.random_walk()        
        boss.check_edges()
        check_aliens_bottom(ai_settings,stats,screen,ship,aliens,
                            bullets,sb,boss)
        if pygame.sprite.spritecollideany(boss,bullets):
            stats.level += 1
            stats.score += 100
            sb.prep_score()
            sb.prep_level()#及时更新屏幕的等级信息需要通过此函数然后给绘制函数调用
            #重置boss的位置为初始位置，别提了，换成函数更新就是不能成
            boss.rect.x = ai_settings.screen_width / 2
            boss.rect.y = 30
            #清空子弹
            bullets.empty()
            #每次消灭boss后创建新的敌人群
            create_fleet(ai_settings,screen,ship,aliens)