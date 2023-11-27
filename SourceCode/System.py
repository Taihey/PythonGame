import random
import pygame
import gamefile

pygame.init() 
frameRate = 15
highScore = 0

pause = False                  #ポーズ画面かどうか 動きを止める
window_x = 600
window_y = 600
field_x = 12000                #x = 0を原点としたときの長さ
field_y = 2000                 #y = 0を原点としたときの高さ
g = 10  

#Timerで制御する時間、TextやAudioで使う
tmr = 0                        #場面転換などに使う
audiotmr = 0                   #bgmの途中からの再生に使う
onfield = False

index = 0                      #シーンの管理

class Timer:                   #時間を管理するクラス 
    def __init__(self):
        self.fr = frameRate    #15
        self.globTimer = 0     #クリアタイムをカウント
        self.ins = []
        self.actTime = 0       #秒数で表す
        self.txt = "---:---.---"
        self.bestTimeText = "---:---.---" 
        self.c = [True, True, True]
        
        global tmr
        tmr = 0                #シーンの切り替えのたびに呼び出す
    
    def initiate(self):       
        self.fr = frameRate    
        self.globTimer = 0    
        self.ins = []
        self.actTime = 0      
        self.txt = "---:---.---"
        
        self.c = [True, True, True]
        
        global tmr
        tmr = 0
        global audiotmr        #ロードでだけ初期化する
        audiotmr = 0
    
    def pauseGame(self):
        global pause
        pause = True
    
    def cancelPause(self):
        global pause
        pause = False
    
    def addLocalTimer(self, instance):
        self.ins.append(instance)
    
    def resetLocalTimer(self):
        self.ins = []
    
    def count(self, string):
        global tmr
        global audiotmr
        
        if pause == False:
            if self.c[0]:
                if string == "system":
                    tmr += 1
                    if onfield:
                        audiotmr += 1/frameRate
        
            if self.c[1]:
                if string == "global":
                    self.globTimer += 1
                    self.actTime += 1/self.fr
                    self.txt = "{:0>2}:{:0>2}.{:0>2}".format(
                        int(int(self.actTime)/60), int(self.actTime) % 60, int((self.actTime) * 100) % 100
                    )
        
            if self.c[2]:
                if string == "local":
                    for i in range(len(self.ins)):
                        self.ins[i].tmr += 1
    
    def reset(self, string):
        global tmr
        if string == "system":
            tmr = 0
        elif string == "global":
            self.globTimer = 0
    
    def stop(self, string):
        if string == "system":
            self.c[0] = False
            
        elif string == "global":
            self.c[1] = False
            
        elif string == "local":
            self.c[2] = False
        
        elif string == "all":
            self.c = [False, False, False]
        
    def start(self):
        self.c = [True, True, True]
    
    def setTimerUI(self, bg, font, col, x, y):
        if index in [-1, 0, 0.5]:
            Text("Time: ---:---.---").putFlex(bg, font, col, x, y)
        else:
            Text("Time: " + self.txt).putFlex(bg, font, col, x, y)       #経過時間を表示
    
    def showBestTimeUI(self, bg, font, col, x, y):
        Text("Best Time: " + self.bestTimeText).putFlex(bg, font, col, x, y) 

class ScoreManager:
    def __init__(self):
        self.file = gamefile.scoreFile
    
    def loadScore(self, tmr):
        global highScore
        fr = open(self.file, 'rb')
        loadedScore = int.from_bytes(fr.readline(), byteorder="big")
        highScore = loadedScore
        fr.close()
        
        if loadedScore == 0:
            tmr.bestTimeText = "---:---.---"
        else:
            time = loadedScore/frameRate
            min = int(time/60)
            sec = time - 60*min
            tmr.bestTimeText = "{:0>2}:{:0>2}.{:0>2}".format(min, int(sec), int(sec*100) % 100)
        return loadedScore                         #フレーム数で返す

    def saveScore(self, score):                    #フレーム数で指定
        if score < highScore or highScore == 0:    #クリアタイムが最小だったら保存
            try:
                data = score.to_bytes(5, "big", signed=False)
                fw = open(self.file, 'wb')
                fw.write(data)
                fw.close()
            except:
                return
    
    def deleteScore(self, tmr):
        global highScore
        highScore = 0
        data = highScore.to_bytes(1, "big", signed=False)
        fw = open(self.file, 'wb')
        fw.write(data)
        fw.close()
        tmr.bestTimeText = "---:---.---" 

class Camera:                             #移動シーンを表示
    def __init__(self, x, y):      
        self.x = x                        #中心の座標を格納
        self.y = y
        self.viewObj = {1 : []}           #奥行きを表すaの値と、それに属するオブジェクト配列
        self.sortedKey = [1]              #aを昇順に並べた配列
    
    def setScene(self, hierarchy):        #カメラで写すオブジェクトをセットする
        self.viewObj = {1:[]}
        self.sortedKey = [1]
        for obj in hierarchy:
            if (obj != None):
                self.viewObj.setdefault(obj.a, [])
                self.viewObj[obj.a].append(obj)
                self.sortedKey = sorted(self.viewObj.keys())
        return self
    
    def display(self, bg):
        rLimit = int(1.5*field_x - (self.x - window_x/2))       #複製表示するときの右端
        bLimit = int(1.2*field_y - (self.y - window_y/2))       #右端
        for i in self.sortedKey:
            for obj in self.viewObj[i]:
                #window上での座標を求める。(左上からの距離) カメラが[window_x/2, window_y/2]で揃っているとする
                x = obj.x - obj.a*(self.x - window_x/2)
                y = obj.y - obj.a*(self.y - window_y/2)
                dx = obj.figure.get_width()
                dy = obj.figure.get_height() 
                if obj.tag == "pic":                      #左上の座標を指定している
                    bg.blit(obj.figure, [x, y])
                elif obj.tag == "bump":                   #右に複製して表示する
                    span = 300
                    for i in range(int(x), rLimit, int(span*obj.a)):
                        bg.blit(obj.figure, [i-dx/2, y-dy])
                elif obj.tag == "floor":
                    for i in range(int(x), int(x) + (obj.right - obj.x), dx):
                        bg.blit(obj.figure, [i-dx/2, y])
                elif obj.tag == "column":                 #下に複製して表示する
                    for i in range(int(y), bLimit, dy):
                        bg.blit(obj.figure, [x-dx/2, i])
                else:
                    bg.blit(obj.figure, [x-dx/2, y-dy])
    
    def chase(self, target):
        self.x = target.x 
        self.y = target.y - 200
        if self.x - window_x/2 < 0:
            self.x = window_x/2
        if self.y > window_y/2:
            self.y = window_y/2

class BtlCamera(Camera):               #バトルシーンを撮影
    def __init__(self, x, y):
        super().__init__(x, y)
        self.centerx = x               #揺れた時に戻る位置
        self.centery = y
    
    def display(self, bg):
        for i in self.sortedKey:
            for obj in self.viewObj[i]:
                x = (obj.btlx + obj.delx) - obj.a*(self.x - window_x/2)
                y = (obj.btly + obj.dely) - obj.a*(self.y - window_y/2)
                dx = obj.figure.get_width()
                dy = obj.figure.get_height() 
                if obj.tag == "center":                   #中心の座標を指定している
                    bg.blit(obj.figure, [x-dx/2, y-dy/2])
                else:                                     #足元の座標を指定
                    bg.blit(obj.figure, [x-dx/2, y-dy])
    
    def shake(self, emy):                                      #敵から攻撃を受けた時に揺れる
        if tmr >= 6:
            delx = random.randint(-int(emy.attack/7), int(emy.attack/7))
            dely = random.randint(-int(emy.attack/7), int(emy.attack/7))
            self.x = self.centerx + delx
            self.y = self.centery + dely
        elif tmr >= 11:
            self.x = self.centerx
            self.y = self.centery 

class Audio:
    def __init__(self):
        self.SEs = gamefile.SEs
        self.BGMs = gamefile.BGMs
        self.state = 0             #流すBGMを変える
        
        self.loadedSEs = []
        for SE in self.SEs:
            self.loadedSEs.append(pygame.mixer.Sound(SE))
    
    def setState(self, state):     
        global audiotmr
                                  #ボスを倒す度に新しいbgmを最初から流す
        if self.state < state:
            self.state = state
            audiotmr = 0    
    
    def playSE(self, string):
        if string == "click":
            self.loadedSEs[0].play()
        elif string == "recover":
            self.loadedSEs[1].play()
        elif string == "powerUp":
            self.loadedSEs[2].play()
    
    def playMusic(self, string):
        global onfield
        
        self.stopMusic()
        
        time = 0
        if string == "field":     #フィールドのbgmは中断しても途中から流す
            onfield = True
            if self.state == 0: 
                pygame.mixer.music.load(self.BGMs[6])
                time = int(audiotmr) % 12
            elif self.state == 1:
                pygame.mixer.music.load(self.BGMs[7])
                time = int(audiotmr) % 26
            elif self.state == 2:
                pygame.mixer.music.load(self.BGMs[8])
                time = int(audiotmr) % 26
        else:
            onfield = False
            if string == "title":
                pygame.mixer.music.load(self.BGMs[0])
            elif string == "gameClear":
                pygame.mixer.music.load(self.BGMs[1])
            elif string == "gameOver":
                pygame.mixer.music.load(self.BGMs[2])
            elif string == "battle":
                pygame.mixer.music.load(self.BGMs[3])
            elif string == "bossBattle":
                pygame.mixer.music.load(self.BGMs[4])
            elif string == "finalBossBattle":
                pygame.mixer.music.load(self.BGMs[5])
        
        pygame.mixer.music.play(loops=-1, start=time)
    
    def stopMusic(self):
        if pygame.mixer.music.get_busy() == True:        
            pygame.mixer.music.stop()

class SceneManager:
    def __init__(self):
        self.loadedIndex = 0    #保持しておくシーン番号
        #ここで表示するオブジェクトを管理する
        self.Hierarchy1 = []                 
        self.Hierarchy2 = [None, None, None] #0:plr, 1:emy, 2:btlBG
    
    def moveScene(self, idx):
        global index
        index = idx
        Timer().reset("system")
    
    def loadNextScene(self, idx):
        self.loadedIndex = idx
    
    def loadScene(self):
        global index
        index = self.loadedIndex
        self.loadedIndex = 0
        
    def addHierarchy(self, string, *obj):
        if string == "field":                 #加えるオブジェクトを指定
            self.Hierarchy1.append(obj[0])
        elif string == "battle":               #indexと加えるオブジェクトを指定
            self.Hierarchy2[obj[0]] = obj[1]
    
    def initHierarchy(self, string):
        if string == "field":
            self.Hierarchy1 = []
        elif string == "battle":
            self.Hierarchy2[0] = None
            self.Hierarchy2[1] = None

class keyManager:
    def __init__(self, key):
        self.key = key
        self.flag = True
    
    def onPress(self):        #押した瞬間だけTrueを返す
        key = pygame.key.get_pressed()
        if key[self.key]:
            ans = self.flag and key[self.key]
            self.flag = False
            return ans
        else:
            self.flag = True
            return False
        

def CollisonJudge(sceneManager):
    for obj in sceneManager.Hierarchy1:
        obj.onGround = False                   #ここで変えて、直後に上書きされるかどうかで着地を判定
    #Collider同士の衝突を検知する--------------------------------
    for i in range(len(sceneManager.Hierarchy1)):
        #衝突判定を持っているものだけを考える
        if sceneManager.Hierarchy1[i].haveCollider:
            self = sceneManager.Hierarchy1[i]
            for j in range(len(sceneManager.Hierarchy1)):
                if j == i:
                    continue
                #相手も衝突判定を持っていたら衝突を判定する
                if sceneManager.Hierarchy1[j].haveCollider:
                    opponent = sceneManager.Hierarchy1[j]
                    #衝突した時の処理
                    if self.collider.judge(opponent.collider):
                        self.onCollision(opponent, sceneManager)

class Text:
    def __init__(self, txt):
        self.text = txt
    
    def putCenter(self, bg, fntsize, col):                      #画面の中心
        font = pygame.font.Font(None, fntsize)
        text = font.render(self.text, True, col)
        bg.blit(text, [window_x/2-text.get_width()/2, window_y/2-text.get_height()/2])
    
    def putHeight(self, bg, fntsize, col, y):                    #中心の高さを指定
        font = pygame.font.Font(None, fntsize)
        text = font.render(self.text, True, col)
        bg.blit(text, [window_x/2-text.get_width()/2, y-text.get_height()/2])
    
    def putFlex(self, bg, fntsize, col, x, y):               #x座標もy座標も変えられる。左上の座標を指定する
        font = pygame.font.Font(None, fntsize)
        text = font.render(self.text, True, col)
        bg.blit(text, [x, y])
    
    #移動するテキスト:System.tmrを0にしてから使う-----------------
    def moveCenter(self, bg, fntsize, col):
        font = pygame.font.Font(None, fntsize)
        text = font.render(self.text, True, col)
        if tmr < 7:              #右端から中心の50px右まで6カウントで移動
            bg.blit(
                text, 
                [window_x - tmr*(window_x-(window_x/2-text.get_width()/2+50))/6, 
                 window_y/2-text.get_height()/2]
                )
        elif tmr < 14:           #中心の100pxを7カウントで移動
            bg.blit(
                text, 
                [((window_x/2-text.get_width()/2)+50) - (tmr-6)*100/7, 
                 window_y/2-text.get_height()/2]
                )
        else:                    #最初と同じ速さで移動
            bg.blit(
                text, 
                [((window_x/2-text.get_width()/2)-50) - (tmr-13)*(window_x-(window_x/2-text.get_width()/2)+50)/6, 
                 window_y/2-text.get_height()/2]
                )

    def moveFlex(self, bg, fntsize, col, y):         #高さを指定できる
        font = pygame.font.Font(None, fntsize)
        text = font.render(self.text, True, col)
        if tmr < 7:
            bg.blit(
                text, 
                [window_x - tmr*(window_x-(window_x/2-text.get_width()/2+50))/6, 
                 y-text.get_height()/2]
                )
        elif tmr < 14:
            bg.blit(
                text, 
                [((window_x/2-text.get_width()/2)+50) - (tmr-6)*100/7, 
                 y-text.get_height()/2]
                )
        else:
            bg.blit(
                text, 
                [((window_x/2-text.get_width()/2)-50) - (tmr-13)*(window_x-(window_x/2-text.get_width()/2)+50)/6, 
                 y-text.get_height()/2]
                )
    
    def insertCenter(self, bg, fntsize, col):
        font = pygame.font.Font(None, fntsize)
        text = font.render(self.text, True, col)
        if tmr < 7:             #中心まで6カウントで移動
            bg.blit(
                text, 
                [window_x - tmr*(window_x-(window_x/2-text.get_width()/2))/6, 
                 window_y/2-text.get_height()/2]
                )
        else:                   #中心で止まる
            bg.blit(
                text, 
                [window_x/2-text.get_width()/2,
                 window_y/2-text.get_height()/2]
                )