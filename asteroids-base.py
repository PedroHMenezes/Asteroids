# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias.
import pygame
import random
import time
from os import path

# Estabelece a pasta que contem as figuras.
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# Dados gerais do jogo.
WIDTH = 480 # Largura da tela
HEIGHT = 600 # Altura da tela
FPS = 60 # Frames por segundo

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
#Classe jogador representando a nave
class Player (pygame.sprite.Sprite):
    
    #Construtor da CLasse
    def __init__ (self):
        
        #Construtor da classe pai (Sprite).
        pygame.sprite.Sprite._init_(self)
        
        #Carregando a imagem de fundo
        player_img=pygame.iamge.load(path.join(img_dir,"playerShip1_orange.png")).convert()
        self.image = player_img
        
        #Diminuindo o tamanho da imagem
        self.image = pygame.transform.scale(player_img(50,38))
        
        #Deixando transparente
        self.image.set_colorkey(BLACK)
        
        #Detalhes sobre o posicionamento
        self.rect = self.image.get_rect()
        
        #Centraliza embaixo da tela
        self.rect.centerx=WIDTH/2
        self.rect.bottom=HEIGHT-10
        
        #Velocidade da nave
        self.speedx=0
        
        #Melhora a colisão entre o meteoro e a nave
        self.radius = 25
        
    #Metodo que atualiza a posição da nave
    def update(self):
        self.rect.x += self.speedx
        
        #Mantém dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left=0

class meteoro (pygame.sprite.Sprite):
    def __init__ (self):
        pygame.sprite.Sprite._init_(self)
        player_img=pygame.image.load(path.join(img_dir,"meteorBrown_med1")).conver()
        self.image = player_img
        self.image=pygame.transform.scale(player_img(50,38))
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.rect.centerx= random.randrange()
        self.rect.centery=[-100,-40]
        self.speedy=[2,9]
        self.speedx=[-3,3]
        self.radius=int(self.rect.width*.85/2)
        
    def update (self):
        self.rect.x+=self.speedx
        self.rect.y+=self.speedy
# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("Asteroids")

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega o fundo do jogo
background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()

#Carrega som
pygame.mixer.music.load(path.join(snd_dir,"tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.4)
boom_sound = pygame.mixer.Sound (path.join(snd_dir,'expl3.wav'))

#Cria uma nave. O construtor será chamado automaticamente
player=Player()
mob=meteoro()
#Cria um grupo de sprites e chama a nave
all_sprites= pygame.sprite.Group()
all_sprites.add(player)

#Criando grupo de mobs
mobs=pygame.sprite.Group()
i=0
while i<8:
    all_sprites.add(player)
    mobs.add(mob)
    i+=1
# Comando para evitar travamentos.
try:
    
    # Loop principal.
    pygame.mixer.music.play(loops=-1)
    running = True
    while running:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            
            # Verifica se foi fechado
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                #Dependendo da tecla adiciona velocidade
                if event.key == pygame.K_LEFT:
                    player.speedx = -8
                if event.key == pygame.K.RIGHT:
                    player.speedx= 8
            #Verifica se parou de apertar a tecla
            if event.type == pygame.KEYUP:
                #Dependendo da tecla, altera a velocidade
                if event.key==pygame.K_LEFT:
                    player.speedx=0
                if event.key==pygame.K_RIGHT:
                    player.speedx=0
        #Atualiza a ação de cada sprite
        all_sprites.update()
        
        #Verifica se houve colisão entre nave e meteoro
        hits=pygame.sprite.spritecollide(player,mobs,False,pygame.sprite.collide_circle)
        if hits:
            #Toca o som da colisão
            boom_sound.play()
            time.sleep(1)
            
            running = False
    
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    pygame.quit()
