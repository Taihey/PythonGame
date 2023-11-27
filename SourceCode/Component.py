import pygame
import System

pygame.init()

class Animator:
    def __init__(self, belong):
        self.belong = belong
        self.img = None
        self.loadedImg = []
    
    def setImg(self, img):
        self.img = img
    
    def load(self, s, f):              #self.imgの範囲を指定
        self.reset()
        for i in range(s, f+1):
            self.loadedImg.append(pygame.image.load(self.img[i])) 
        #print(self.belong.tag + "'s img is loaded")
    
    def reset(self):
        self.loadedImg = []
    
    def play(self, tmr, s, f, v):               #self.loadedImgの範囲 tmrは親オブジェクトと同期してもらう。
        len = f - s + 1
        if (self.loadedImg != []):
            return self.loadedImg[s + int(tmr*v) % len]
    
    def rPlay(self, tmr, s, f, v):
        len = f - s + 1
        return self.loadedImg[f - int(tmr*v) % len]

    def scaledPlay(self, tmr, s, f, v, r):
        len = f - s + 1
        img = self.loadedImg[s + int(tmr*v) % len]
        ix = img.get_width()
        iy = img.get_height()
        return pygame.transform.scale(img, [ix*r, iy*r])

class Audio:
    def __init__(self, belong):
        self.SEs = []
        self.loadedSEs = {
            "jump": None,
            "attack": None
            }
        self.belong = belong
    
    def setSE(self, ses):
        self.SEs = ses
        self.loadedSEs["jump"] = pygame.mixer.Sound(self.SEs[0])
        self.loadedSEs["attack"] = pygame.mixer.Sound(self.SEs[1])
        return self
    
    def playSE(self, string):
        self.loadedSEs[string].play()

class BoxCollider:
    def __init__(self, belong):
        self.width = 0
        self.height = 0
        self.belong = belong
        self.delx = 0                #所属先の足元の座標からどれだけずれるか
        self.dely = 0
        
        self.leftPos = self.belong.x - self.width/2
        self.rightPos = self.belong.x + self.width/2
        self.topPos = self.belong.y - self.height
        self.bottomPos = self.belong.y
    
    def setDelta(self, delta):
        self.delx = delta[0]         
        self.dely = delta[1]
        
        return self
    
    def movePos(self, string):     
        if string == "UpperLeft":     #左上に合わせる
            self.delx = self.width/2
            self.dely = - self.height
            
            self.leftPos = self.belong.x
            self.rightPos = self.belong.x + self.width
            self.topPos = self.belong.y
            self.bottomPos = self.belong.y + self.height
        
        elif string == "reset":
            self.delx = 0
            self.dely = 0
            
            self.leftPos = self.belong.x - self.width/2
            self.rightPos = self.belong.x + self.width/2
            self.topPos = self.belong.y - self.height
            self.bottomPos = self.belong.y
        
        return self
            
    def setSize(self, width, height):   #upperLeftへのmovePosはやり直す
        self.width = width
        self.height = height
        
        self.leftPos = self.belong.x - self.width/2 + self.delx
        self.rightPos = self.belong.x + self.width/2 + self.delx
        self.topPos = self.belong.y - self.height + self.dely
        self.bottomPos = self.belong.y + self.dely
        
        return self
    
    def judge(self, opponent):
        if (self.width == 0 and self.height == 0) or (opponent.width == 0 and opponent.height == 0):
            return False
        #相手が中
        h1 = self.leftPos <= opponent.rightPos and opponent.rightPos <= self.rightPos
        h2 = self.leftPos <= opponent.leftPos and opponent.leftPos <= self.rightPos
        #自分が中
        h3 = opponent.leftPos <= self.rightPos and self.rightPos <= opponent.rightPos
        h4 = opponent.leftPos <= self.leftPos and self.leftPos <= opponent.rightPos
        #下向きが正
        v1 = self.bottomPos >= opponent.topPos and opponent.topPos >= self.topPos
        v2 = self.bottomPos >= opponent.bottomPos and opponent.bottomPos >= self.topPos
        v3 = opponent.bottomPos >= self.topPos and self.topPos >= opponent.topPos
        v4 = opponent.bottomPos >= self.bottomPos and self.bottomPos >= opponent.topPos
        return ((h1 or h2) or (h3 or h4)) and ((v1 or v2) or (v3 or v4)) 