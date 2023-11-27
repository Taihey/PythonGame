import pygame
import Component 
import System

pygame.init()  
key = pygame.key.get_pressed() 
window_x = System.window_x
window_y = System.window_y
g = 10  

BLACK  = (  0,   0,   0)

#すべての親クラス
class GameObject: 
    def __init__(self):
        self.x = 0              #位置
        self.y = 0 
        self.isKinetic = False  #重力を受けるかどうか
        self.vx = 0             #横移動の速さ
        self.vy = 0             #縦方向の変化量 下向きが正
        self.onGround = False   #地面に触れているかどうか
        
        self.onBtl = False
        self.btlx = 0           #バトルシーンでの基準の位置
        self.btly = 0
        self.delx = 0           #バトルシーンでの移動量
        self.dely = 0
        
        self.animator = Component.Animator(self)
        self.figure = None      #ロードした、そのフレームで表示する画像
        
        self.audioPlayer = Component.Audio(self)
        
        self.collider = Component.BoxCollider(self)
        self.haveCollider = False
        
        self.a = 1              #奥行きを表す
        self.tag = None
        
        self.tmr = 0            #アニメーション用
    
    def setValue(self, keys, values):
        for i in range(len(keys)):
            if keys[i] == "x":
                self.x = values[i]
            elif keys[i] == "y":
                self.y = values[i]
            elif keys[i] == "kinetic":
                self.isKinetic = values[i]
            elif keys[i] == "btlx":
                self.btlx = values[i]
            elif keys[i] == "btly":
                self.btly = values[i]
            elif keys[i] == "img":
                self.animator.setImg(values[i])
            elif keys[i] == "se":
                self.audioPlayer.setSE(values[i])
            elif keys[i] == "boxCol":
                self.collider.setSize(values[i][0], values[i][1])
            elif keys[i] == "moveCol":
                self.collider.movePos(values[i])
            elif keys[i] == "haveCol":
                self.haveCollider = values[i]
            elif keys[i] == "a":
                self.a = values[i]
            elif keys[i] == "tag":
                self.tag = values[i]
        return self
    
    def copy(self):
        return GameObject().setValue(
            ["x", "y", "btlx", "btly", "img", "a"], 
            [self.x, self.y, self.btlx, self.btly, self.img, self.a]
            )
    
    def shift(self, string, delta):              #当たり判定も一緒にずらす
        if string == "x":
            self.x += delta
            if self.haveCollider:
                self.collider.setSize(self.figure.get_width(), self.figure.get_height())
        elif string == "y":
            self.y += delta                      #delta>0 だと下にずらす
            if self.haveCollider:
                self.collider.setSize(self.figure.get_width(), self.figure.get_height())
    
    def Play(self):                              #アニメーションを動かす
        self.figure = self.animator.play(self.tmr, 0, 0, 1)
    
    def move(self):                              #位置、姿、判定を動かす
        if self.onBtl == False:
            if self.isKinetic:                   #重力によって落ちる 落としてからgを足す
                self.y += self.vy
                self.vy += g 
            self.x += self.vx
            
            self.Play()
            if self.haveCollider:
                self.collider.setSize(self.figure.get_width()*0.8, self.figure.get_height()*0.8)
    
    def onCollision(self, opponent, sceneManager):    #衝突を判定した時の処理(moveの後に実行される)
        if opponent.tag == "floor":
            
            deltau = self.collider.bottomPos - opponent.collider.topPos
            deltal = self.collider.rightPos - opponent.collider.leftPos
            deltar = opponent.collider.rightPos - self.collider.leftPos
            #上から衝突した場合は上に乗る
            if deltau <= self.vy + g:
                if System.pause == False:
                    self.onGround = True              #CollisionJudgeの先頭の代入を上書き
                self.shift("y", -deltau)
                self.vy = 0
            #左の方が近かったら左にずれる
            elif deltal < deltar:
                self.shift("x", -deltal)
            else:
                self.shift("x", deltar)
                
#playerを表すクラス-------------
class Player(GameObject):
    def __init__(self, life, attack):       
        super().__init__()
        self.isKinetic = True
        
        self.state = 0                #バトルシーンでの状態を表す          
        self.life = life
        self.lifemax = life
        self.attack = attack
        self.defense = 1
        self.portion = 0
        
        #戦闘シーン
        self.btlx = window_x/4
        self.btly = window_y/2 + 100
        self.emy = None               #対戦相手
        
        self.tag = "Player"
    
    #移動シーン loadするのは0 ~ 10------------------------   
    #ボタンによって実行 (main関数 衝突判定の後)
    def walk(self, vx, vx2):          #地上の移動速度と空中移動速度を指定 
        if self.onGround:             #ボタンを離しても動きっぱなし
            self.vx = vx
        else:
            self.vx = vx2
    
    def stop(self):
        self.walk(0, 0)
        
    def jump(self, vy0):              #上向きの速度を指定
        if self.onGround:
            self.vy = -vy0                
            self.resetTimer()
            self.audioPlayer.playSE("jump")
    
    def recover(self, a):
        self.life += a
        if self.life > self.lifemax:
            self.life = self.lifemax
    
    #戦闘シーン ロード画像: 11 ~ 17-----------------
    def setEnemy(self, emy):
        self.emy = emy
        return self
        
    def stay(self):
        self.delx = 0
        self.dely = 0  
        
    def Attack(self, x, y):           #self.tmrを0にしてから行う
        if self.tmr < 3:              #攻撃時の位置の変化と敵へダメージの付与
            self.stay()
        elif 3 <= self.tmr and self.tmr < 8:
            self.delx = (self.tmr-2)*x/5 
            self.dely = (self.tmr-2)*y/5
        elif 8 <= self.tmr and self.tmr < 11:
            self.delx = x - (self.tmr-7)*x/5 
            self.dely = y - (self.tmr-7)*y/5
        else:
            self.stay()  
        
        if self.tmr == 6:
            self.emy.life -= self.attack
            if self.emy.life < 0:
                self.emy.life = 0
            self.audioPlayer.playSE("attack")          
    
    def intoBattle(self):
        self.onBtl = True
        self.resetTimer()
    
    def exitBattle(self):
        self.onBtl = False
        self.resetTimer()
    
    #バトルから逃げる
    def escape(self):
        self.exitBattle()
        self.emy.exitBattle()
        
        orient = -1
        if self.emy.x < self.x:
            orient = 1
        self.x += orient * 80     
        self.vx = orient * 10
        
    #敵を突き飛ばす
    def pushEnemy(self):
        self.exitBattle()
        self.state = 0
        self.emy.exitBattle()
        if self.emy.x < self.x:
            orient = -1
        else:
            orient = 1
        self.emy.x += orient * 100
        self.emy.y -= 1                          #地面から浮かせることで、orientを変えられないようにする
        self.emy.jump(50)
    
    def levelUp(self):
        self.recover(10*self.emy.experience)
        self.defense += 0.1*self.emy.experience          #守備力を上昇させる
        self.attack += 2*self.emy.experience             #攻撃力を上げる
        self.portion += 1*self.emy.experience            #回復薬をゲット
    
    def winBattle(self, emy):               #勝利時、バトルから抜け出す瞬間
        self.exitBattle()
        self.stop()
        emy.exitBattle()
        
        self.resetTimer()
        emy.resetTimer()              
                       
    #アニメーションを再生する
    def Play(self):
        if self.onBtl == False:             
            if self.onGround:
                if self.vx > 0:
                    self.figure = self.animator.play(self.tmr, 0, 3, 1/3)
                elif self.vx < 0:
                    self.figure = self.animator.play(self.tmr, 4, 7, 1/3)
                elif self.vx == 0:
                    self.figure = self.animator.play(self.tmr, 8, 8, 1)

            else:            
                if self.vx > 0:
                    self.figure = self.animator.play(self.tmr, 9, 9, 1)
                elif self.vx < 0:
                    self.figure = self.animator.play(self.tmr, 10, 10, 1)
                elif self.vx == 0:
                    self.figure = self.animator.play(self.tmr, 9, 9, 1)
        
        else:
            if self.state == 4:               #バトルシーンでのゲームオーバー時 17
                self.figure = self.animator.play(self.tmr, 0, 0, 1)
        
            elif self.state == 5:             #stay()とせっと
                self.figure = self.animator.play(self.tmr, 0, 0, 1)
            
            elif self.state == 6:             #attack()とセット
                if self.tmr < 3:     
                    self.figure = self.animator.play(self.tmr, 0, 0, 1)
                elif 3 <= self.tmr and self.tmr < 8:
                    self.figure = self.animator.play(self.tmr-3, 1, 5, 1)
                elif 8 <= self.tmr and self.tmr < 11:
                    self.figure = self.animator.rPlay(self.tmr-8, 1, 5, 1)
                else:
                    self.figure = self.animator.play(self.tmr, 0, 0, 1)  
    
    def move(self):
        #playerの座標を決定
        super().move()
        
        if self.tag == "Player":      #Enemyへの継承用
            if self.onBtl:     
                if self.state == 4:
                    self.stay()
                elif self.state == 5:
                    self.stay()
                elif self.state == 6:
                    self.Attack(150, 80)
        
                #再生 
                self.Play()
    
    def setState(self, string):        #main関数内で変更する状態
        if string == "stay":
            self.state = 5
        elif string == "attack":       #場面の切り替わりで使う
            self.state = 6
            self.resetTimer()
        elif string == "dead":
            self.state = 4
    
    def resetTimer(self):
        self.tmr = 0
    
    def onCollision(self, opponent, sceneManager):
        super().onCollision(opponent, sceneManager)
        
        if self.tag == "Player":      #Enemyへの継承用の条件付け
            if opponent.tag in ["Enemy", "B1", "B2", "B3", "BF"]:
                sceneManager.moveScene(1.5)
                sceneManager.addHierarchy("battle", 0, self)
                sceneManager.addHierarchy("battle", 1, opponent)
                self.setEnemy(sceneManager.Hierarchy2[1])              #Player
                opponent.setEnemy(sceneManager.Hierarchy2[0])              #敵
                #Playerの方が高かったら先攻
                if self.y < opponent.y:    
                    sceneManager.loadNextScene(2)
                else:
                    sceneManager.loadNextScene(3)
            
    #UI-------------------------
    def drawPortion(self, bg, portion):
        #所持している回復薬を表示
        for x in range(self.portion):
            bg.blit(portion, 
                    [250 + (portion.get_width() + 10)*(x % 10),    #1行10個
                     20 + (portion.get_height() + 10)*(int)(x / 10)])
        
    def drawPortionFlex(self, bg, portion, x, y):
        bg.blit(portion, [x, y])
    
    def drawLife(self, bg, x, y):             #左上の座標を指定
        ratio = self.life/self.lifemax
        #画面の左上に体力を配置する
        pygame.draw.rect(bg, BLACK, [x-2, y-2, 200 + 4, 24])
        pygame.draw.rect(bg, [255*(1-ratio), 255*ratio, 255*ratio*ratio*ratio], [x, y, 200*ratio, 20])
    
#敵を表すクラス--------------------
class Enemy(Player):
    def __init__(self, life, attack, experience):
        super().__init__(life, attack)  
        self.experience = experience                     #経験値 倒したときの、playerの成長量を決める
        
        self.btlx = window_x * 3/4
        self.btly = window_y/2 + 150
        
        self.tag = "Enemy"
    
    def copy(self):                   #vxやvx2を外部でいじらない前提
        return Enemy(self.life, self.attack, self.experience).setValue(
            ["x", "y", "btlx", "btly", "img", "se", "haveCol", "a", "tag"], 
            [self.x, self.y, self.btlx, self.btly, self.animator.img, self.audioPlayer.SEs, self.haveCollider, self.a, self.tag]
            ).setEnemy(self.emy)
    
    #移動シーン ロードするのは0 ~ 15----------
    def dead(self):          #当たり判定をなくす
        self.setValue(["haveCol", "kinetic"], [False, False])
    
    #戦闘シーン 16 ~ 23
    def Attack(self, x, y):  #self.tmrを0にしてから行う
        if self.tmr < 3:     
            self.stay()
        elif 3 <= self.tmr and self.tmr < 8:
            self.delx = - (self.tmr-2)*x/5 
            self.dely = - (self.tmr-2)*y/5
        elif 8 <= self.tmr and self.tmr < 11:
            self.delx = - x + (self.tmr-7)*x/5 
            self.dely = - y + (self.tmr-7)*y/5
        else:
            self.stay()
        
        if self.tmr == 6:
            self.emy.life -= self.attack/self.emy.defense
            if self.emy.life < 0:
                self.emy.life = 0
            self.audioPlayer.playSE("attack")   
    
    #移動シーンでの動き 衝突判定の後にやる
    def setMove(self):                         #playerを追いかけ続ける jumpはしない
        #追ってくる範囲を制限する    
        #空中では速度を維持
        if self.emy.x > self.x and self.x > self.emy.x-window_x and self.state != 4:             
            self.walk(2, self.vx)
        elif self.emy.x < self.x and self.x < self.emy.x + window_x and self.state != 4:
            self.walk(-2, self.vx)
        #範囲外では止まる
        else: 
            self.stop()     
    
    def Play(self):
        if self.onBtl == False:    
            #生きてるとき          
            if self.vx >= 0:
                self.figure = self.animator.play(self.tmr, 0, 5, 1/4)
            elif self.vx < 0:
                self.figure = self.animator.play(self.tmr, 6, 11, 1/4)
            #倒したら上書き
            if self.state == 4:             #倒れる演出   
                if self.tmr < 12:
                    self.figure = self.animator.play(self.tmr, 12, 14, 1/4)
                else:
                    self.figure = self.animator.play(self.tmr, 15, 15, 1)
        else:                
            if self.state == 4:               #バトルシーンでのやられ ロード画像: 12
                self.figure = self.animator.scaledPlay(self.tmr, 0, 0, 1, 2)
            elif self.state == 5:             #stay()
                self.figure = self.animator.play(self.tmr, 0, 0, 1)
            elif self.state == 6:             #attack()
                if self.tmr < 3:     
                    self.figure = self.animator.play(self.tmr, 0, 0, 1)
                elif 3 <= self.tmr and self.tmr < 10:
                    self.figure = self.animator.play(self.tmr-3, 1, 7, 1)
                elif 10 <= self.tmr and self.tmr < 17:
                    self.figure = self.animator.rPlay(self.tmr-10, 1, 7, 1)
                else:
                    self.figure = self.animator.play(self.tmr, 0, 0, 1)  
    
    def move(self):
        super().move()
        #画像の座標、状態を決定------
        
        if self.onBtl == False:     
            if self.state == 4:
                self.dead()
        else:
            if self.state == 4:
                self.stay()
            elif self.state == 5:
                self.stay()
            elif self.state == 6:
                self.Attack(150, 80)
        
        self.Play()
     
    def onCollision(self, opponent, sceneManager):   #Playerとの衝突はPlayerの方で考える
        super().onCollision(opponent, sceneManager)
        if opponent.tag == "Enemy":
            ori = 1                       #selfの方が右: 1, 左: -1
            if self.x < opponent.x:       #colliderも一緒にずらさないといけない
                ori = -1
            #衝突しなくなるまで横にずらす
            while self.collider.judge(opponent.collider):
                self.shift("x", ori)
                opponent.shift("x", -ori)
    
    def drawLife(self, bg, x, y):        #右上の座標を指定
        pygame.draw.rect(bg, BLACK, [window_x-(x-2)-204, window_y-(x-2)-24 - 50, 200 + 4, 24])
        ratio = self.life/self.lifemax
        pygame.draw.rect(bg, [255*(1-ratio), 255*ratio, 255*ratio*ratio*ratio], 
                         [window_x-x-200*ratio, window_y-y-20 - 50, 200*ratio, 20])
        
#ラスボス 倒したときのアニメーションを加える
class FinalBoss(Enemy):
    def __init__(self, life, attack, experience):
        super().__init__(life, attack, experience)  

    def Play(self):
        if self.onBtl == False:               
            if self.vx >= 0:
                self.figure = self.animator.play(self.tmr, 0, 5, 1/4)
            elif self.vx < 0:
                self.figure = self.animator.play(self.tmr, 6, 11, 1/4)
        else:
            if self.state == 4:             #バトルシーンで倒れるアニメーションを流す 12~15
                if self.tmr < 12:
                    self.figure = self.animator.play(self.tmr, 0, 2, 1/4)
                else:
                    self.figure = self.animator.play(self.tmr, 3, 3, 1)
            
            elif self.state == 5:             
                self.figure = self.animator.play(self.tmr, 0, 0, 1)
            elif self.state == 6:            
                if self.tmr < 3:     
                    self.figure = self.animator.play(self.tmr, 0, 0, 1)
                elif 3 <= self.tmr and self.tmr < 10:
                    self.figure = self.animator.play(self.tmr-3, 1, 7, 1)
                elif 10 <= self.tmr and self.tmr < 17:
                    self.figure = self.animator.rPlay(self.tmr-10, 1, 7, 1)
                else:
                    self.figure = self.animator.play(self.tmr, 0, 0, 1)  

#静止しているものを表すクラス-------        
class Object(GameObject):                                                       
    def __init__(self, scaled):
        super().__init__()
        self.tag= "obj"
        self.scaled = scaled
    
    def Play(self):                  #アニメーションを動かす
        if self.scaled:
            self.figure = self.animator.scaledPlay(self.tmr, 0, 0, 1, self.a)
        else: 
            self.figure = self.animator.play(self.tmr, 0, 0, 1)

class Floor(GameObject):             #長方形の床 幅を指定
    def __init__(self, left, right, ground):
        super().__init__()
        self.tag = "floor"
        self.x = left
        self.right = right
        self.y = ground
        
        self.collider = Component.BoxCollider(self).setSize(
            (self.right-self.x), (2000 - self.y)
            ).movePos("UpperLeft")
        self.haveCollider = True
    
    def move(self):                   #当たり判定を位変化させない
        self.Play()
    
    def onCollision(self, opponent, sceneManager):
        return