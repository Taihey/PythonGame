import gameclass
import gamefile
import System   

window_x = 600
window_y = 600

field_x = System.field_x    
field_y = System.field_y     

steps = [-100, 0, 500, 700, 1000, 1200, 1500, 1800, 2000, 2500, 3000, 3200, 
         3400, 4000, 4500, 5000, 5300, 5500, 6000, 6200,
         6400, 6550, 6750, 6900, 7000, 7300, 7700, 8000, 8300, 8800, 9100, 
         9200, 9300, 9400, 9500, field_x, field_x+50]                                       #区切りの位置
grounds = [-field_y, 510, 480, 400, 450, 350, 300, 200, 100, 150, 50, 
           -50, -150, -200, -300, -400, -500, -450, -500,
           -600, -700, -800, -850, -900, -1000 ,-1050 ,-1100 ,-1200, -1150, -1200,
           -1300, -1400, -1500, -1550, 550, -field_y]

def ConstructObjects():
    #表示するオブジェクトをまとめる
    objects = []   #移動シーン パラメーターが変化しないもののみ
    
    #地形
    Floors = []
    for i in range(len(grounds)):
        Floors.append(
            gameclass.Floor(steps[i], steps[i + 1], grounds[i]).setValue(
                ["img"],
                [gamefile.flrPic]
                )
            )
        objects.append(Floors[-1])
        Floors[-1].animator.load(0, 0)
    
    Columns = []
    for i in range(2, len(grounds)):              #floorの両脇に柱を立てる
        Columns.append(
            gameclass.Object(False).setValue(
            ["x", "y", "img", "tag"],
            [steps[i], grounds[i], gamefile.colPic,"column"]
            )
        )
        objects.append(Columns[-1])
        Columns[-1].animator.load(0, 0)
        
        Columns.append(
            gameclass.Object(False).setValue(
            ["x", "y", "img", "tag"],
            [steps[i+1], grounds[i], gamefile.colPic,"column"]
            )
        )
        objects.append(Columns[-1])
        Columns[-1].animator.load(0, 0)
    
    #動かないもの(背景)------
    BG = [
        gameclass.Object(False).setValue(
            ["x", "y", "img", "a", "tag"], 
            [0, window_y - 500, gamefile.backGround[0], 0.1, "pic"]
            ),
        gameclass.Object(False).setValue(
            ["x", "y", "img", "a", "tag"],
            [0, window_y - 1000, gamefile.backGround[1], 0.1, "pic"]
            ),
        gameclass.Object(False).setValue(
            ["x", "y", "img", "a", "tag"],
            [700, window_y - 500, gamefile.backGround[0], 0.1, "pic"]
            ),
        gameclass.Object(False).setValue(
            ["x", "y", "img", "a", "tag"],
            [700, window_y - 1000, gamefile.backGround[1], 0.1, "pic"]
            ),
        gameclass.Object(False).setValue(                  #月
            ["x", "y", "img", "a"],
            [1000, -200, gamefile.backGround[2], 0.15]
            )
    ]
    
    for bg in BG:
        bg.animator.load(0, 0)
    for bg in BG:
        objects.append(bg)
        
    kanban = gameclass.Object(False).setValue(
            ["x", "y", "img", "a"],
            [300, 510, gamefile.boardPic, 0.95]
            )
    kanban.animator.load(0, 0)
    objects.append(kanban)
    
    bumps = [
        gameclass.Object(True).setValue(
            ["x", "y", "img", "a", "tag"],
            [0, window_y, gamefile.bumPic, 0.9, "bump"]
            ),
        gameclass.Object(True).setValue(
            ["x", "y", "img", "a", "tag"],
            [100, window_y, gamefile.bumPic, 0.6, "bump"]
            ),
        gameclass.Object(True).setValue(
            ["x", "y", "img", "a", "tag"],
            [200, window_y, gamefile.bumPic, 0.7, "bump"]
            ),
        gameclass.Object(True).setValue(
            ["x", "y", "img", "a", "tag"],
            [0, window_y, gamefile.bumPic, 1.3, "bump"]
            )      
    ]
    for bump in bumps:
        bump.animator.load(0, 0)
    for bump in bumps:
        objects.append(bump)
    
    return objects

def ConstructPlayer():
    plr  = gameclass.Player(100, 50).setValue(
        ["x", "y", "img", "se", "haveCol"],
        [100, 500, gamefile.plr_image, [gamefile.jump_se, gamefile.plr_se], True]
    )
    
    return plr

def ConstructEnemies(plr):
    enemies = []
                
    #出現する敵の種類をまとめる
    enemy0 = gameclass.Enemy(80, 10, 1, ).setValue(
        ["img", "se", "haveCol"],
        [gamefile.emy0_image, [gamefile.jump_se2, gamefile.emy_se], True]
    ).setEnemy(plr)
    enemy1 = gameclass.Enemy(150, 20, 2).setValue(
        ["img", "se", "haveCol"],
       [gamefile.emy1_image, [gamefile.jump_se2, gamefile.emy_se], True]
    ).setEnemy(plr)
    enemy2 = gameclass.Enemy(250, 70, 2).setValue(
        ["img", "se", "haveCol"],
        [gamefile.emy5_image, [gamefile.jump_se2, gamefile.plr_se], True]
    ).setEnemy(plr)
    enemy3 = gameclass.Enemy(500, 100, 4).setValue(
        ["img", "se", "haveCol"],
        [gamefile.emy4_image, [gamefile.jump_se2, gamefile.emy_se3], True]
    ).setEnemy(plr)
    boss1 = gameclass.Enemy(300, 70, 5).setValue(
        ["x", "y", "img", "se", "haveCol", "tag"],
        [2900, -1500, gamefile.emy2_image, [gamefile.jump_se2, gamefile.emy_se2], True, "B1"]
    ).setEnemy(plr)
    boss2 = gameclass.Enemy(700, 110, 7).setValue(
        ["x", "y", "img", "se", "haveCol", "tag"],
        [5900, -1500, gamefile.emy2_image, [gamefile.jump_se2, gamefile.emy_se2], True, "B2"]
    ).setEnemy(plr)
    boss3 = gameclass.Enemy(900, 220, 10).setValue(
        ["x", "y", "img", "se", "haveCol", "tag"],
        [8700, -1500, gamefile.emy2_image, [gamefile.jump_se2, gamefile.emy_se2], True, "B3"]
    ).setEnemy(plr)
    finalBoss = gameclass.FinalBoss(1500, 300, 10).setValue(
        ["x", "y", "img", "se", "haveCol", "tag"],
        [11500, -1500, gamefile.emy3_image, [gamefile.jump_se2, gamefile.emy_se4], True, "BF"]
    ).setEnemy(plr)
                
    #リストに格納する
    for pos in [900, 1400, 1800, 10300]:
        enemies.append(enemy0.setValue(["x", "y"], [pos, -1500]).copy())
    for pos in [1200, 1600, 2200, 2500, 9900, 10500]:
        enemies.append(enemy1.setValue(["x", "y"], [pos, -1500]).copy())
    for pos in [3400, 3700, 4100, 4300, 5200, 6800, 8300, 10200, 11000]:
        enemies.append(enemy2.setValue(["x", "y"], [pos, -1500]).copy())
    for pos in [4800, 6300, 7000, 7500, 7700, 8000]:
        enemies.append(enemy3.setValue(["x", "y"], [pos, -1500]).copy())
    enemies.append(boss1)
    enemies.append(boss2)
    enemies.append(boss3)
    enemies.append(finalBoss)
    
    return enemies

def ConstructBtlBG():
    #バトルシーン
    btlBG = gameclass.Object(False).setValue(
            ["btlx", "btly", "img", "a", "tag"], 
            [window_x/2, window_y/2, gamefile.bg2, 0.95, "center"]
            )
    btlBG.animator.load(0, 0)
    
    return btlBG