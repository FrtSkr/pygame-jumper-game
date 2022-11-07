import pygame
from settings import *

vector = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.image.load("ScreenImg/santaClaus.png")
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.vx = vector(0,0) # karakterimizin hızı, ivmeli harekette kullanılacak
        self.acc = vector(0,0.3) # ivmeli harekette kullanacağımız ivmemiz 
    
    def jump(self):
        self.rect.y += 1
        isContact = pygame.sprite.spritecollide(self, self.game.platforms, False) # sıçrayıştan önce platformla temas kontrolü
        if isContact:
            self.game.jumpEffect.play()
            self.vx.y -= 18
        
    def update(self, *args):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a] or keys[pygame.K_d]: # sağ ya da sol hareket kontrolü
            if keys[pygame.K_d]:
                if self.vx.x < 7: # ivmeli hareket için kontrol
                    self.acc.x = 0.5
                else:
                    self.acc.x = 0
                
            if keys[pygame.K_a]: # ivmeli hareket için kontrol
                if self.vx.x > -7:
                    self.acc.x = -0.5
                else:
                    self.acc.x = 0  
        
            self.vx.x += self.acc.x
            
        else: # karakterimizin hareketi sonrası sürtünme kuvveti ile durması için ayarlamalar
            if self.vx.x > 0:
                self.vx.x -= 0.5
            if self.vx.x < 0:
                self.vx.x += 0.5
        
        self.vx.y += self.acc.y # y ekseninde sabit ivmeli hareketimiz
        
        self.rect.x += self.vx.x 
        self.rect.y += self.vx.y
        
        if self.rect.right >= WIDTH: # ekran dışına çıkışı kontrol ettik
            self.rect.right = WIDTH - 1
            self.vx.x -= 0.5
        if self.rect.left <= 0: # ekran dışına çıkışı kontrol ettik
            self.rect.left = 1
            self.vx.x += 0.5
            
class Platform(pygame.sprite.Sprite): # platformlarımızı yaratmak için iskelet yapımız
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w,h))
        self.image.fill((255,255,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        

class Point(pygame.sprite.Sprite):
    def __init__(self, game, platform):
        super().__init__()
        self.game = game
        self.platform = platform
        self.image = pygame.image.load("theme/coin.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.platform.rect.midtop
        
    def update(self,*args):
        self.rect.midbottom = self.platform.rect.midtop # altın görselini platformun ortasına yerleştirdik
        
        if not self.game.platforms.has(self.platform):  # platformlar aşağı kayıp yok olduğunda altınları da yok ettik
            self.kill()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        