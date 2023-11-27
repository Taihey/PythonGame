#操作方法をまとめたスクリプト
import pygame
import System   

#押した瞬間だけ反応するキーの作成---
keyManager_r = System.keyManager(pygame.K_r)
keyManager_j = System.keyManager(pygame.K_j)
keyManager_SPACE = System.keyManager(pygame.K_SPACE)
keyManager_UP = System.keyManager(pygame.K_UP)
keyManager_p = System.keyManager(pygame.K_p)

#sキーを押してタイトルからフィールドへ
def titleOperation(sceneManager, audioPlayer, timer):
    key = pygame.key.get_pressed()
    if key[pygame.K_s] or keyManager_p.onPress():
        sceneManager.moveScene(0.5)         
        audioPlayer.playSE("click")
    elif key[pygame.K_e] or key[pygame.K_q]: 
        sceneManager.moveScene(-1)
        audioPlayer.playSE("click")
    elif key[pygame.K_d] and key[pygame.K_l] and key[pygame.K_t]:
        System.ScoreManager().deleteScore(timer)
        audioPlayer.playSE("click")

#移動シーンでのジャンプ、横移動
def fieldOperation(plr, audioPlayer):
    key = pygame.key.get_pressed()
    #Playerの操作、Enemyの移動--------
    if keyManager_j.onPress() or keyManager_SPACE.onPress():
        plr.jump(50)
    if keyManager_UP.onPress():
        plr.jump(30)
                
    if key[pygame.K_RIGHT]:
        plr.walk(10, 20)
    elif key[pygame.K_LEFT]:
        plr.walk(-10, -20)
    else:
        plr.stop()
            
    if keyManager_r.onPress():
        if plr.portion > 0 and plr.life < plr.lifemax:
            plr.portion -= 1
            plr.recover(20)
            audioPlayer.playSE("recover")

#バトルシーンでの操作
def battleOperation(plr, sceneManager):
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE] == 1:            #逃げる
        sceneManager.moveScene(1)
        plr.escape()
    elif key[pygame.K_DOWN] == 1:           #敵を突き放す
        sceneManager.moveScene(1)
        plr.pushEnemy()
    elif key[pygame.K_a] == 1:              #攻撃へ
        sceneManager.moveScene(2.5)
        plr.setState("attack")

def toTitle(sceneManager, audioPlayer):
    key = pygame.key.get_pressed()
    if key[pygame.K_f] or key[pygame.K_t]:
        sceneManager.moveScene(0)
        audioPlayer.playSE("click")

def pauseGame(audioPlayer):
    key = pygame.key.get_pressed()
    if keyManager_p.onPress():
        System.Timer().pauseGame()
        audioPlayer.playSE("click")

def pauseOperation(sceneManager, audioPlayer):
    key = pygame.key.get_pressed()
    if keyManager_p.onPress() or key[pygame.K_x]:
        System.Timer().cancelPause()
        audioPlayer.playSE("click")
        
    elif key[pygame.K_f] or key[pygame.K_t]:
        sceneManager.moveScene(0)
        System.Timer().cancelPause()
        audioPlayer.playSE("click")