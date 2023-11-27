import pygame
import sys 
import System   
import Constructor
import Operation
import UI
 
BLACK  = (  0,   0,   0)
window_x = System.window_x
window_y = System.window_x
       
#main関数--------------------------- 
def main(): 
    pygame.init()
    pygame.display.set_caption("Punch Man")
    screen = pygame.display.set_mode((window_x, window_y)) 
    #surface = pygame.Surface((window_x, window_y))
    clock = pygame.time.Clock()
    
    #オブジェクトのインスタンスを生成
    sceneManager = System.SceneManager()
    timer = System.Timer()
    audioPlayer = System.Audio()
    camera = System.Camera(window_x/2, window_y/2)
    btlCamera = System.BtlCamera(window_x/2, window_y/2)
    
    #存在だけ宣言
    plr = None
    enemies = []
    
    #------------------------
    audioPlayer.playMusic("title")
    System.ScoreManager().loadScore(timer)  #ベストスコアをロード
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        timer.count("global")
        timer.count("system")
        timer.count("local")
 
        screen.fill(BLACK)
        
        #ポーズするかどうか 
        if System.pause == False:
            if not System.index in [-1, 0, 0.5]:
                Operation.pauseGame(audioPlayer)
        else:
            Operation.pauseOperation(sceneManager, audioPlayer)
            if System.index == 0:
                audioPlayer.playMusic("title")
        
        #シーンごとの動き-----------
        if System.index == 1:            #カメラに写すのは、衝突判定してから
            #オブジェクトの座標を決める
            if System.pause == False:    #ポーズ中は動かさない
                for obj in sceneManager.Hierarchy1:
                    obj.move()
            
        elif System.index > 1:
            if System.pause == False:
                for obj in sceneManager.Hierarchy2:
                    obj.move()
            #カメラに写す
            btlCamera.display(screen)
        #-------------------------
        if System.index == -1:           #終了
            if System.tmr > 1*System.frameRate:
                pygame.quit()
                sys.exit()     
        
        if System.index == 0:             #タイトル                  
            Operation.titleOperation(sceneManager, audioPlayer, timer)
            
            if System.index == 0.5:
                sceneManager.initHierarchy("field")
                continue
        
        elif System.index == 0.5:        #ロード 
            #ヒエラルキーで管理するインスタンスの生成-------------
            if System.tmr == 1:
                plr = Constructor.ConstructPlayer()
                sceneManager.addHierarchy("field", plr)

                enemies = Constructor.ConstructEnemies(plr)
                for enemy in enemies:
                    sceneManager.addHierarchy("field", enemy)      
                
            elif System.tmr == 2:
                objects = Constructor.ConstructObjects()
                for obj in objects:
                    sceneManager.addHierarchy("field", obj)

                btlBG = Constructor.ConstructBtlBG()
                sceneManager.addHierarchy("battle", 2, btlBG) 
                
            elif System.tmr == 3:    
                #シーンをセット
                camera.setScene(sceneManager.Hierarchy1)
                btlCamera.setScene(sceneManager.Hierarchy2)
                
                #idx1で使う画像を読み込む--------
                plr.animator.load(0, 10)         
                for i in range(len(enemies)):
                    enemies[i].animator.load(0, 15)
                #-------------------------------
                
                audioPlayer.__init__()
                audioPlayer.playMusic("field")

            elif System.tmr == 4:
                timer.initiate()   #タイマーを初期化
                for i in range(len(enemies)):
                    timer.addLocalTimer(enemies[i])
                timer.addLocalTimer(plr)
                sceneManager.moveScene(1)
                                
                continue      
        
        if System.index == 1:                               #フィールド
            
            #Collider同士の衝突の検知とその時の処理--------------
            System.CollisonJudge(sceneManager)
            
            #速度を決めるだけ、動かすのはmove()
            Operation.fieldOperation(plr, audioPlayer)
            #Playerの位置に合わせて敵も動く
            for enemy in enemies:
                enemy.setMove()
            
            #画面上の位置を決める
            camera.chase(plr)
            camera.display(screen)
            
            if System.index == 1.5:
                btlCamera.setScene(sceneManager.Hierarchy2)
                        
                plr.intoBattle()
                plr.setState("stay")
                plr.emy.intoBattle()
                plr.emy.setState("stay")
                    
                if plr.emy.tag == "BF":                       #ラスボス戦のbgm
                    audioPlayer.playMusic("finalBossBattle")
                elif plr.emy.tag in ["B1", "B2", "B3"]:       #ボス戦のbgm
                    audioPlayer.playMusic("bossBattle")
                else:                                         #通常戦闘bgm
                    audioPlayer.playMusic("battle")
                                
                #戦闘シーンで使う画像を読み込む--------
                plr.animator.load(11, 16)
                plr.emy.animator.load(16, 23)
                #------------------------------------
                continue
        
        elif System.index == 1.5:                            #Encounter 見合ってる時間
            if System.tmr >= 20:
                sceneManager.loadScene()
                if System.index == 3:
                    plr.setState("stay")
                    plr.emy.setState("attack")
                timer.reset("system")
                
                continue
                    
        #バトル-------------------------------------------------------
        elif System.index == 2:                              #バトル 自分のターン 入力待ち
            Operation.battleOperation(plr, sceneManager)
            
            if System.index == 1:
                #idx1で使う画像を読み込む--------
                plr.animator.load(0, 10)       
                plr.emy.animator.load(0, 15)
                #-------------------------------
                sceneManager.initHierarchy("battle")
                
                audioPlayer.playMusic("field")
                
                continue
            
            elif System.index == 2.5:
                timer.reset("system")
                
                continue
                
        elif System.index == 2.5:                            #プレイヤーの攻撃
            if System.tmr > 15:
                plr.setState("stay")
                
                if plr.emy.life > 0:                         #敵の攻撃
                    sceneManager.moveScene(3)                         
                    
                    plr.emy.setState("attack")
                    timer.reset("system")
                    
                    continue
                
                else: 
                    plr.emy.setState("dead")
                    if plr.emy.tag == "B1":
                        audioPlayer.setState(1)
                    if plr.emy.tag == "B2":
                        audioPlayer.setState(2)
                    if plr.emy.tag == "B3":
                        audioPlayer.setState(2)
                    
                    if plr.emy.tag == "BF":   #ラスボスを倒したらクリア画面に移る
                        sceneManager.moveScene(5)                     
                        timer.reset("system")
                        
                        plr.emy.animator.load(12, 15)  
                        plr.emy.resetTimer()  
                        
                        audioPlayer.stopMusic()
                        
                        continue
                    
                    else:
                        sceneManager.moveScene(2.7)          
                        
                        plr.emy.animator.load(12, 12)    
                                                    
                        timer.reset("system")
                        audioPlayer.stopMusic()
                        audioPlayer.playSE("powerUp")
                        
                        continue
        
        elif System.index == 2.7:                     #power upを知らせる
            if System.tmr == 1:
                plr.levelUp()
            
            if System.tmr >= 20:
                sceneManager.moveScene(1)
                plr.winBattle(plr.emy)                #パワーアップ
                timer.reset("system")
                
                plr.emy.resetTimer()
                
                #idx1で使う画像を読み込む--------
                plr.animator.load(0, 10)         
                plr.emy.animator.load(0, 15)
                #-------------------------------
                sceneManager.initHierarchy("battle")
                
                audioPlayer.playMusic("field")
                    
                continue
                
        
        elif System.index == 3:                        #敵のターン
            btlCamera.shake(plr.emy)                   #敵の攻撃によって揺れる
            if System.tmr > 15:                     
                if plr.life > 0:                       #自分の攻撃
                    sceneManager.moveScene(2)
                    plr.setState("stay")
                    plr.emy.setState("stay")
                    timer.reset("system")         
                    
                    continue
                
                else:
                    timer.reset("system")
                    
                    plr.animator.load(17, 17)
                    
                    plr.setState("dead")
                    sceneManager.moveScene(4)          #ゲームオーバー
                    
                    continue
        
        elif System.index == 4:                        #プレイヤーが倒れる
            timer.stop("global")                       #プレイ時間測定をやめる
            if System.tmr >= 10:
                audioPlayer.playMusic("gameOver")
                sceneManager.moveScene(4.5)   
                
                continue
        
        elif System.index == 4.5:                      #入力待ち
            Operation.toTitle(sceneManager, audioPlayer)
            
            if System.index == 0:
                timer.start()                          #タイマーを動かしてから戻る
                 
                audioPlayer.playSE("click")
                #あえて音楽は流しっぱなしにする
                
                continue
        
        elif System.index== 5:                              #ラスボスが倒れる
            timer.stop("global")                            #タイム計測終了
            
            if System.tmr >= 20:
                sceneManager.moveScene(5.5)
                System.ScoreManager().saveScore(timer.globTimer)  #ベストタイムだったら保存 
                
                audioPlayer.playMusic("gameClear")
                
                continue
        
        elif System.index == 5.5:             #Game Clear
            if System.tmr >= 20:     #リザルト
                sceneManager.moveScene(5.6)   
                
                continue
        
        elif System.index == 5.6:             #ClearTime
            if System.tmr >= 20:
                sceneManager.moveScene(5.7)
                
                continue
        
        elif System.index == 5.7:             #入力待ち
            Operation.toTitle(sceneManager, audioPlayer)
            
            if System.index == 0:
                timer.start()
                
                audioPlayer.playSE("click")
                
                sceneManager.initHierarchy("battle")
                System.ScoreManager().loadScore(timer)
                
                continue
            
        UI.drawUI(screen, plr, timer)
        
        pygame.display.update()                   
        clock.tick(System.frameRate)
        
if __name__ == '__main__':
    main()