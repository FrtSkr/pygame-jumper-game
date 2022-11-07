import pygame,sys,random
from sprites import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Ekranımızı yarattık
        pygame.display.set_caption(TITLE) # Oyunumuza isim verdik
        self.clock = pygame.time.Clock() # FPS'te kullanacağımız nesnemiz
        self.running = True # oyunun kapanmasından sorumlu değişken
        self.score = 0
        self.copyX = -1 # platform oluşturma algoritmasında kullandık
        
        self.background = pygame.image.load("ScreenImg/sky.png")
        self.jumpEffect = pygame.mixer.Sound("Effect/jump.flac")
        self.fallEffect = pygame.mixer.Sound("Effect/fall.wav")
        self.clickEffect = pygame.mixer.Sound("Effect/click.wav")
        self.flyEffect = pygame.mixer.Sound("Effect/fly.flac")
        self.coinSplashEffect = pygame.mixer.Sound("Effect/coinsplash.ogg")
        
    def new(self):
        self.all_sprites = pygame.sprite.Group() # Oyun içindeki spritelarımızı grupladık
        self.platforms = pygame.sprite.Group() # platform sprite grubumuz
        self.points = pygame.sprite.Group() # puan nesnemizin grubu
        platform0 = Platform(0, HEIGHT - 30, WIDTH, 40) # platformlarımızı yarattık
        platform1 = Platform(WIDTH - 350, 50, 100, 15)
        platform2 = Platform(WIDTH - 550, 150, 100, 15)
        platform3 = Platform(WIDTH - 150, 250, 100, 15)
        platform4 = Platform(WIDTH - 500, 450, 100, 15)
        platform5 = Platform(WIDTH - 100, 550, 100, 15)
        
        self.platforms.add(platform0)
        self.platforms.add(platform1)
        self.platforms.add(platform2)
        self.platforms.add(platform3)
        self.platforms.add(platform4)
        self.platforms.add(platform5)
      
        
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.all_sprites.add(platform0)
        self.all_sprites.add(platform1)
        self.all_sprites.add(platform2)
        self.all_sprites.add(platform3)
        self.all_sprites.add(platform4)
        self.all_sprites.add(platform5)
        self.run()
    
    def run(self): # Oyun başlatıldığında koşulacak fonksiyonumuz
        self.playing = True 
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
            self.update()
            
    def level(self, s): # skorumuzu ekrana yazacak olan fonksiyonumuz
        font = pygame.font.SysFont("Century Gothic", 25)
        text = font.render(s, True, (255,255,255))
        self.screen.blit(text, (WIDTH / 2 - (text.get_size()[0] / 2), 0)) # ekranın ortasına bastırdık
        
            
    def draw(self): # Görüntüleri çizdireceğimiz fonksiyonumuz
        self.screen.blit(self.background, self.background.get_rect())
        self.level("Score : {}".format(self.score))
        self.all_sprites.draw(self.screen) # oluşturduğumuz spriteları ekrana çizecek
        self.screen.blit(self.player.image, self.player.rect)
        
    
    def loginScreen(self): # giriş ekranımız
        loginImg = pygame.image.load("ScreenImg/LoginScreen.png")
        self.screen.blit(loginImg, loginImg.get_rect())  
        pygame.display.update()
        self.holdOn()
        
    def endScreen(self): # bitiş ekranımız
        endImg = pygame.image.load("ScreenImg/EndScreen.png")
        self.screen.blit(endImg, endImg.get_rect()) 
        
        font = pygame.font.SysFont("Century Gothic", 32)
        text = font.render("Score : {}".format(self.score), True, (255,255,255))
        self.screen.blit(text, (WIDTH / 2 - (text.get_size()[0] / 2), HEIGHT / 2))
        
        pygame.display.update()
        self.holdOn()
    
    def holdOn(self): # giriş ve bitiş ekranlarındaki bekleme ve tuş kontrolü
        wait = True
        while wait:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False
                    self.running = False
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: # basılan tuş ENTER ise
                        self.clickEffect.play()
                        self.score = 0
                        wait = False
    
    def update(self): # spriteları güncelleyip ekranı ona göre ayarlayacak olan fonk.
        self.all_sprites.update() # bütün spriteların update metodu çağrıldı.
        
        
        if self.player.vx.y > 0: # karakterin y eksenindeki hareketi 0 dan büyükse: aşağı doğru harekerini ifade ediyor.
            collisions = pygame.sprite.spritecollide(self.player, self.platforms, dokill=False) # karakterimiz platformla etkileşime girdiğinde bize bildirecek olan yapı
        
            if collisions:
                self.player.vx.y = 0 # eğer platformla bir etkileşim varsa y eksenindeki hareketi sıfırladık
                self.player.rect.bottom = collisions[0].rect.top # ve karakterimizin alt kısmını platformun üst kısmına eşitledik ki karakter platformun içine giremesin.
            
           
        if self.player.vx.y < 0: # karakterin y eksenindeki hareketi 0 dan küçükse: yukarı doğru harekerini ifade ediyor.
            collisions = pygame.sprite.spritecollide(self.player, self.platforms, dokill=False) # karakterimiz platformla etkileşime girdiğinde bize bildirecek olan yapı
            if collisions: # sıçrayış anında bir platforma çarptıysak
                self.player.vx.y = 0 # y eksenindeki hızımız sıfırlanır
                self.player.rect.top = collisions[0].rect.bottom 
          
        touchPoint = pygame.sprite.spritecollide(self.player, self.points, True) # Karakterimizin puan nesnemize dokunup dokunmadığını kontrol ediyoruz.  
        if touchPoint:
            self.coinSplashEffect.play()
            self.score += 20
        
        if self.player.rect.top < HEIGHT / 4: # platform aşağıya kaydırma işlemi
            self.player.rect.y += max(abs(self.player.vx.y), 3)
            for platform in self.platforms:
                platform.rect.y += max(abs(self.player.vx.y), 3)
                if platform.rect.top >= HEIGHT:
                    platform.kill()
        
        while len(self.platforms) < 6: # platform yukarı kaydıkça aşağıda kalan platformlar yok olacağı için
            width = random.randrange(50, 100) # en başta olan paltform sayısını kontrol ettirip ekranım yukarı kaydıkça
            height = random.randrange(10, 20) #  yazdığım algoritma ile düzenli yeni platformlar oluşacaktır.            
            x = random.randrange(0, WIDTH - width) 
            y = -130
            if x == self.copyX or abs(x - self.copyX) < 250 or abs(x - self.copyX) > 300:
                loop = True
                while loop:
                    if x == self.copyX or abs(x - self.copyX) < 250 or abs(x - self.copyX) > 300: # yaratılan platformların bir öncekiyle arasındaki mesafeyi ayarladım
                        x = random.randrange(0, WIDTH - width)                        
                    else:
                        loop = False
                         
            self.copyX = x
            
            p = Platform(x, y, width, height)
            self.platforms.add(p)
            self.all_sprites.add(p)
            
            if random.randint(1,3) == 1: # altın çıkma olasılığı 1/3
                point = Point(self, p)
                self.points.add(point)
                self.all_sprites.add(point)
            
        if self.player.rect.top > HEIGHT: # Burada karakterimizin düşüşünü kontrol ettik
            self.fallEffect.play() # düşüş efekti
            for sprite in self.all_sprites: # karakter düşerken bütün spritelarımı
                sprite.rect.y -= max(self.player.vx.y, 15) # y ekseninde 15 birim yukarı kaydırdım
                if sprite.rect.bottom < 0: # spritelarım ekran yüksekliğinin dışında ise
                    sprite.kill() # spriteları yokettik.
        if len(self.platforms) == 0: 
            self.playing = False # oyununun tekrar başlamasını sağlayan yapı
            
        pygame.display.update() 
    
    def events(self): # oyun içindeki eventları toplayacak olan fonk.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()
                
            if event.type == pygame.KEYDOWN: # space tuşuna basıldığında sıçrayış fonksiyonunu çağırır.
                if event.key == pygame.K_SPACE:
                    self.player.jump()
