from game import *

game = Game() # game objesi yaratıldı
game.loginScreen() # giriş ekranı fonksiyonu çağrıldı
while game.running: 
    game.new()
    game.endScreen()