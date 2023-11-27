from pathlib import Path

def bd():
    return Path("./GameFiles")

flrPic = [bd()/"floors/floor.png"]
colPic = [bd()/"floors/column.png"]
#竹
bumPic = [bd()/"objects/bump.png"]
#背景画像
backGround = [
    [bd()/"objects/nightSky.png"],
    [bd()/"objects/nightSky2.png"],
    [bd()/"objects/moon.png"]
]
bg2 = [bd()/"picture/battleBG.png"]

#看板
boardPic = [bd()/"objects/kanban.png"]

#プレイヤーと敵
plr_image = [  
    #フィールド
    bd()/"player/player.png", bd()/"player/player2.png", bd()/"player/player3.png", bd()/"player/player4.png",       #右走り
    bd()/"player/player5.png", bd()/"player/player6.png", bd()/"player/player7.png", bd()/"player/player8.png",      #左走り
    bd()/"player/player9.png", bd()/"player/player10.png", bd()/"player/player11.png",                            #ステイ&ジャンプ
    #バトル
    bd()/"player/player12.png", bd()/"player/player13.png", bd()/"player/player14.png", bd()/"player/player15.png", 
    bd()/"player/player16.png", bd()/"player/player17.png", bd()/"player/player18.png"                            
    ] 
emy0_image = [
    #フィールド
    bd()/"enemies/enemy0/enemy0_4.png", bd()/"enemies/enemy0/enemy0_4.png", bd()/"enemies/enemy0/enemy0_5.png", bd()/"enemies/enemy0/enemy0_6.png", 
    bd()/"enemies/enemy0/enemy0_6.png", bd()/"enemies/enemy0/enemy0_5.png", 
    bd()/"enemies/enemy0/enemy0_1.png", bd()/"enemies/enemy0/enemy0_1.png", bd()/"enemies/enemy0/enemy0_2.png", bd()/"enemies/enemy0/enemy0_3.png", 
    bd()/"enemies/enemy0/enemy0_3.png", bd()/"enemies/enemy0/enemy0_2.png", 
    bd()/"enemies/enemy0/enemy0_15.png", bd()/"enemies/enemy0/enemy0_15.png", bd()/"enemies/enemy0/enemy0_15.png", bd()/"enemies/enemy0/enemy0_15.png", 
    #バトル
    bd()/"enemies/enemy0/enemy0_7.png", bd()/"enemies/enemy0/enemy0_8.png", bd()/"enemies/enemy0/enemy0_9.png", bd()/"enemies/enemy0/enemy0_10.png", 
    bd()/"enemies/enemy0/enemy0_11.png", bd()/"enemies/enemy0/enemy0_12.png", bd()/"enemies/enemy0/enemy0_13.png", bd()/"enemies/enemy0/enemy0_14.png", 
    ]
emy1_image = [
    #フィールド
    bd()/"enemies/enemy/enemy1_1.png", bd()/"enemies/enemy/enemy1_1.png", bd()/"enemies/enemy/enemy1_2.png", bd()/"enemies/enemy/enemy1_3.png", 
    bd()/"enemies/enemy/enemy1_3.png", bd()/"enemies/enemy/enemy1_4.png", 
    bd()/"enemies/enemy/enemy1_5.png", bd()/"enemies/enemy/enemy1_5.png", bd()/"enemies/enemy/enemy1_6.png", bd()/"enemies/enemy/enemy1_7.png", 
    bd()/"enemies/enemy/enemy1_7.png", bd()/"enemies/enemy/enemy1_8.png", 
    bd()/"enemies/enemy/enemy1_15.png", bd()/"enemies/enemy/enemy1_15.png", bd()/"enemies/enemy/enemy1_15.png", bd()/"enemies/enemy/enemy1_15.png", 
    #バトル
    bd()/"./enemies/enemy/enemy1_9.png", bd()/"./enemies/enemy/enemy1_10.png", bd()/"enemies/enemy/enemy1_10.png", bd()/"enemies/enemy/enemy1_11.png", 
    bd()/"./enemies/enemy/enemy1_12.png", bd()/"./enemies/enemy/enemy1_13.png", bd()/"enemies/enemy/enemy1_14.png", bd()/"enemies/enemy/enemy1_14.png", 
    ]
emy2_image = [
    #フィールド
    bd()/"enemies/enemy2/enemy2_10.png", bd()/"enemies/enemy2/enemy2_11.png", bd()/"enemies/enemy2/enemy2_12.png", bd()/"enemies/enemy2/enemy2_13.png",
    bd()/"enemies/enemy2/enemy2_14.png", bd()/"enemies/enemy2/enemy2_15.png",                                                                     #右歩き
    bd()/"enemies/enemy2/enemy2_16.png", bd()/"enemies/enemy2/enemy2_17.png", bd()/"enemies/enemy2/enemy2_18.png", bd()/"enemies/enemy2/enemy2_19.png", 
    bd()/"enemies/enemy2/enemy2_20.png", bd()/"enemies/enemy2/enemy2_21.png",                                                                     #左歩き
    bd()/"enemies/enemy2/enemy2_22.png", bd()/"enemies/enemy2/enemy2_23.png", bd()/"enemies/enemy2/enemy2_24.png", bd()/"enemies/enemy2/enemy2_25.png", #撃破時
    #バトル 
    bd()/"enemies/enemy2/enemy2_2.png", bd()/"enemies/enemy2/enemy2_3.png", bd()/"enemies/enemy2/enemy2_4.png", bd()/"enemies/enemy2/enemy2_5.png",
    bd()/"enemies/enemy2/enemy2_6.png", bd()/"enemies/enemy2/enemy2_7.png", bd()/"enemies/enemy2/enemy2_8.png", bd()/"enemies/enemy2/enemy2_9.png"
    ]
emy3_image = [
    #フィールド
    bd()/"enemies/enemy3/enemy3_5.png", bd()/"enemies/enemy3/enemy3_6.png", bd()/"enemies/enemy3/enemy3_7.png", bd()/"enemies/enemy3/enemy3_8.png", 
    bd()/"enemies/enemy3/enemy3_7.png", bd()/"enemies/enemy3/enemy3_6.png",                                                                   #右歩き
    bd()/"enemies/enemy3/enemy3_1.png", bd()/"enemies/enemy3/enemy3_2.png", bd()/"enemies/enemy3/enemy3_3.png", bd()/"enemies/enemy3/enemy3_4.png", 
    bd()/"enemies/enemy3/enemy3_3.png", bd()/"enemies/enemy3/enemy3_2.png",                                                                     #左歩き
    bd()/"enemies/enemy3/enemy3_18.png", bd()/"enemies/enemy3/enemy3_19.png", bd()/"enemies/enemy3/enemy3_20.png", bd()/"enemies/enemy3/enemy3_21.png", #撃破時
    #バトル 
    bd()/"./enemies/enemy3/enemy3_9.png", bd()/"./enemies/enemy3/enemy3_10.png", bd()/"enemies/enemy3/enemy3_11.png", bd()/"enemies/enemy3/enemy3_12.png",
    bd()/"./enemies/enemy3/enemy3_13.png", bd()/"./enemies/enemy3/enemy3_16.png", bd()/"enemies/enemy3/enemy3_16.png", bd()/"enemies/enemy3/enemy3_17.png"
    ]
emy4_image = [
    bd()/"enemies/enemy4/enemy4_4.png", bd()/"enemies/enemy4/enemy4_4.png", bd()/"enemies/enemy4/enemy4_5.png", bd()/"enemies/enemy4/enemy4_6.png",
    bd()/"enemies/enemy4/enemy4_6.png", bd()/"enemies/enemy4/enemy4_5.png",
    bd()/"enemies/enemy4/enemy4_1.png", bd()/"enemies/enemy4/enemy4_1.png", bd()/"enemies/enemy4/enemy4_2.png", bd()/"enemies/enemy4/enemy4_3.png",
    bd()/"enemies/enemy4/enemy4_3.png", bd()/"enemies/enemy4/enemy4_2.png",
    bd()/"enemies/enemy4/enemy4_14.png", bd()/"enemies/enemy4/enemy4_15.png", bd()/"enemies/enemy4/enemy4_16.png", bd()/"enemies/enemy4/enemy4_17.png",
    #バトル
    bd()/"./enemies/enemy4/enemy4_7.png", bd()/"./enemies/enemy4/enemy4_8.png", bd()/"enemies/enemy4/enemy4_9.png", bd()/"enemies/enemy4/enemy4_10.png",
    bd()/"./enemies/enemy4/enemy4_11.png", bd()/"./enemies/enemy4/enemy4_12.png", bd()/"enemies/enemy4/enemy4_13.png", bd()/"enemies/enemy4/enemy4_13.png"
]
emy5_image = [
    bd()/"enemies/enemy5/enemy5_1.png", bd()/"enemies/enemy5/enemy5_1.png", bd()/"enemies/enemy5/enemy5_2.png", bd()/"enemies/enemy5/enemy5_3.png",
    bd()/"enemies/enemy5/enemy5_3.png", bd()/"enemies/enemy5/enemy5_4.png",
    bd()/"enemies/enemy5/enemy5_5.png", bd()/"enemies/enemy5/enemy5_5.png", bd()/"enemies/enemy5/enemy5_6.png", bd()/"enemies/enemy5/enemy5_7.png",
    bd()/"enemies/enemy5/enemy5_7.png", bd()/"enemies/enemy5/enemy5_8.png",
    bd()/"enemies/enemy5/enemy5_15.png", bd()/"enemies/enemy5/enemy5_15.png", bd()/"enemies/enemy5/enemy5_15.png", bd()/"enemies/enemy5/enemy5_15.png",
    #バトル
    bd()/"enemies/enemy5/enemy5_9.png", bd()/"enemies/enemy5/enemy5_10.png", bd()/"enemies/enemy5/enemy5_10.png", bd()/"enemies/enemy5/enemy5_11.png",
    bd()/"enemies/enemy5/enemy5_12.png", bd()/"enemies/enemy5/enemy5_13.png", bd()/"enemies/enemy5/enemy5_14.png", bd()/"enemies/enemy5/enemy5_14.png"
]

#SE---------------------
SEs = [
    bd()/"se/title_click.oga",
    bd()/"se/recover.oga",
    bd()/"se/power_up.oga",
    ]
plr_se = bd()/"se/punch.oga"
emy_se = bd()/"se/emy_atk.oga"
emy_se2 = bd()/"se/emy_atk2.oga"
emy_se3 = bd()/"se/emy_atk3.oga"
emy_se4 = bd()/"se/emy_atk4.oga"

jump_se = bd()/"se/jump.oga"
jump_se2 = bd()/"se/jump2.oga"
#BGM--------------------
BGMs = [
    bd()/"music/opening.ogg",                 
    bd()/"music/end.ogg", bd()/"music/end2.ogg",
    bd()/"music/battle.ogg", bd()/"music/boss.ogg", bd()/"music/boss2.ogg",
    bd()/"music/field.ogg", bd()/"music/field2.ogg", bd()/"music/field3.ogg"
    ]

opening = bd()/"picture/opening.png"
portion = bd()/("picture/portion.png")

#データの保存----------
scoreFile = bd()/"Score.dat"