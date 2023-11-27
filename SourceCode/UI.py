#UIの表示 main関数の最後に実行
import pygame
import gamefile
import System   

BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
RED    = (255,   0,   0) 
ORANGE = (255, 128,   0)
BLUE   = (  0,   0, 255)
YELLOW = (255, 255,   0)
AQUA   = (  0, 255, 255)

window_x = System.window_x
window_y = System.window_x

#UIとしての画像
opening = pygame.image.load(gamefile.opening)
portion = pygame.image.load(gamefile.portion)
#pause画面用のスクリーン
pauseScreen = pygame.Surface((window_x, window_y), flags=pygame.SRCALPHA)
pauseScreen.fill((0, 255, 255, 128))
#ロード画面用
loadScreen = pygame.Surface((window_x, window_y), flags=pygame.SRCALPHA)
loadScreen.fill((0, 0, 0, 100))

def drawUI(bg, plr, timer):
    #タイトル背景
    if System.index in [-1, 0, 0.5]:
        bg.blit(opening, [window_x/2-opening.get_width()/2, window_y/2-opening.get_height()/2])
    #ずっとタイムを表示
    if System.index != -1:
        timer.setTimerUI(bg, 30, YELLOW, x=20, y=48)
    #ゲーム終了
    if System.index == -1:
        System.Text("Thank You for Playing!!").putCenter(bg, 70, WHITE)
    #タイトル画面    
    if System.index in [0, 0.5]:
        System.Text("Punch Man").putHeight(bg, 130, WHITE, y=250)
        System.Text("Press [S] or [P] Key To Start!!").putHeight(bg, 50, WHITE, y=400)
        System.Text("Press [E] or [Q] Key To Quit").putHeight(bg, 50, RED, y=500)
        timer.showBestTimeUI(bg, 30, YELLOW, x=20, y=75)
        
        pygame.draw.rect(bg, YELLOW, [265, 43, 265, 57])
        pygame.draw.rect(bg, RED, [263, 41, 269, 61], width=4, border_radius=3)
        System.Text("To Delete Your Best Time,").putFlex(bg, 30, RED, x=270, y=48)
        System.Text("Push [D]+[L]+[T] key").putFlex(bg, 30, RED, x=300, y=75)
    #ロード画面
    if System.index == 0.5:
        bg.blit(loadScreen, [0, 0])
        System.Text("-- Now loading: " + str(System.tmr) + "/3 --").putHeight(bg, 50, WHITE, y=300)
    #タイトル以外    
    if System.index >= 1:
        plr.drawLife(bg, x=20, y=20)      #体力を表示し続ける
        plr.drawPortion(bg, portion)
        pygame.draw.rect(bg, YELLOW, [15, 185, 105, 30])
        pygame.draw.rect(bg, AQUA, [13, 183, 109, 34], width = 4, border_radius=3)
        System.Text("[P]:pause").putFlex(bg, 30, BLUE, x=20, y=190)
        #Playerのパラメーター表示
        pygame.draw.rect(bg, AQUA, [15, 545, 270, 30])
        pygame.draw.rect(bg, ORANGE, [13, 543, 274, 34], width = 4, border_radius=3)
        System.Text("Attack: {0:0.1f}".format(plr.attack/5)).putFlex(bg, 30, RED, x=20, y=550)
        System.Text("Defense: {0:0.1f}".format(plr.defense)).putFlex(bg, 30, BLUE, x=150, y=550)
    #移動シーン    
    if System.index == 1:
        pygame.draw.rect(bg, YELLOW, [15, 70, 211, 106])
        pygame.draw.rect(bg, AQUA, [13, 68, 215, 110], width = 4, border_radius=3)
        System.Text("[RIGHT][LEFT]:move").putFlex(bg, 30, BLUE, x=20, y=75)
        System.Text("[UP]:jump").putFlex(bg, 30, BLUE, x=20, y=100)
        System.Text("[SPACE][J]:big jump").putFlex(bg, 30, BLUE, x=20, y=125)
        System.Text("[R]:").putFlex(bg, 30, BLUE, x=20, y=150)
        plr.drawPortionFlex(bg, portion, x=55, y=150)
        System.Text("recover").putFlex(bg, 30, BLUE, x=80, y=150)
    #バトル突入
    if System.index == 1.5:
        if plr.emy.tag == "BF":
            System.Text("Final Battle!").moveCenter(bg, 120, RED)
        elif plr.emy.tag in ["B1", "B2", "B3"]:
            System.Text("Boss Battle!").moveCenter(bg, 120, RED)
        else:
            System.Text("Encounter").moveCenter(bg, 120, RED)
    #自分のターン    
    if System.index == 2:
        pygame.draw.rect(bg, YELLOW, [15, 70, 215, 81])
        pygame.draw.rect(bg, AQUA, [13, 68, 219, 85], width=4, border_radius=3)
        System.Text("[A]:attack").putFlex(bg, 30, BLUE, x=20, y=75)
        System.Text("[SPACE]:escape").putFlex(bg, 30, BLUE, x=20, y=100)
        System.Text("[DOWN]:push enemy").putFlex(bg, 30, BLUE, x=20, y=125)
    #勝利時    
    if System.index == 2.7:
        System.Text("--LEVEL UP--").moveCenter(bg, 120, AQUA)
    #バトル中 敵の体力を描く    
    if System.index == 2 or System.index == 2.5 or System.index == 3:
        plr.emy.drawLife(bg, 20, 20)
    #体力が0になったとき    
    if System.index == 4.5:
        System.Text("GAME OVER").putCenter(bg, 120, RED)
        System.Text("Press [F] or [T] Key to Go to Title").putHeight(bg, 50, RED, y=400)
    #ラスボスを倒した時    
    if System.index == 5.5:
        System.Text("GAME CLEAR").moveCenter(bg, 120, AQUA)
        
    if System.index == 5.6:
        System.Text("Clear Time" + timer.txt).insertCenter(bg, 80, AQUA)
        
    if System.index == 5.7:
        System.Text("Clear Time" + timer.txt).putCenter(bg, 80, AQUA)
        System.Text("Press [F] or [T] Key to Go to Title!").putHeight(bg, 50, AQUA, y=400)
    
    #ポーズ画面
    if System.pause:
        bg.blit(pauseScreen, [0, 0])
        pygame.draw.rect(bg, YELLOW, [85, 155, 430, 90])
        pygame.draw.rect(bg, AQUA, [82, 152, 436, 96], width=6, border_radius=10)
        System.Text("Pause Menu").putHeight(bg, 100, BLACK, y = 200)
        
        pygame.draw.rect(bg, YELLOW, [50, 350, 500, 100])
        pygame.draw.rect(bg, AQUA, [47, 347, 506, 106], width=6, border_radius=10)
        System.Text("Press [P] or [X] Key to Cancel Pause").putHeight(bg, 40, BLACK, y=370)
        System.Text("Press [F] or [T] Key to Back to Title").putHeight(bg, 40, RED, y=430)