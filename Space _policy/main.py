import pygame
import os,sys,time,random
import const
from random import randint,uniform



'''
Criando os Meteoros Aula 07 Colisão simples
'''





width, height = 1200, 650

#Calcula o tempo de disparo
def laser_timer(pode_disparar,duracao=500):
    if not pode_disparar:
        tempo_corrente = pygame.time.get_ticks()
        if tempo_corrente - tempo_disparo > duracao: 
            pode_disparar =True
    return pode_disparar


def laser_update(laser_list,speed=1200):
    for rec in laser_list:
        rec.y-=round(speed * dt)
        if rec.bottom < 0:
            laser_list.remove(rec)

def meteoro_update(meteoro_list,speed=500):
    for rec_tupla in meteoro_list:
        rec=rec_tupla[0]
        direcao = rec_tupla[1]        
        rec.center += direcao*speed * dt
        if rec.top > height:
            meteoro_list.remove(rec_tupla)


def displayScore(display,font): 
    score_text = str(f'S T A R - GAME  {pygame.time.get_ticks()//1000}')
    texto = font.render(score_text, True,(255,255,225))
    recText = texto.get_rect(midleft=(30,15))
    display.blit(texto, recText)




pygame.init()
width, height = 1200, 650
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("N A S A")

#Carregando as imagens
nave = pygame.image.load(os.path.join("assets","img","lula.png")).convert_alpha()
nave = pygame.transform.scale(nave,(78,70))

#campo = pygame.image.load(os.path.join("assets","img","Campo_de_forca_2-removebg-preview.png")).convert_alpha()
#campo = pygame.transform.scale(campo,(80,75))
#campo.set_alpha(90)

lasersurf = pygame.image.load(os.path.join("assets","img","BolsaPicanha.png")).convert_alpha()
lasersurf =pygame.transform.scale(lasersurf,(40,40))
meteor_img = pygame.image.load(os.path.join("assets","img","jair2.png")).convert_alpha()
meteor_img = pygame.transform.scale(meteor_img,(80,80))
metoros_list = []

laser_list = []
#Capturando o Retangulo 
navRec = nave.get_rect(center=(500,500))
bg1 = pygame.image.load(os.path.join("assets","img","fundo.jpg")).convert()
bgR1 = bg1.get_rect(center=((width/2,(height/2))))

#campo
#capRec = campo.get_rect(center=(500,500))
#cg1 = pygame.image.load(os.path.join("assets","img","fundo.jpg")).convert()
#cgR1 = cg1.get_rect(center=((width/2,(height/2))))
#Criando a Font do jogo
font = pygame.font.Font(os.path.join("assets","Font","Sigmar","Sigmar-Regular.ttf"),16)

pode_disparar = True #verifica se o jogador pode realizar outro dispato
tempo_disparo=pygame.time.get_ticks()


# Criando os meteoros
meteoro_tempo = pygame.event.custom_type()
pygame.time.set_timer(meteoro_tempo, 500) # 0,5 segundos 

#Criando som
#laser_som = pygame.mixer.Sound(os.path.join("assets","sound","laser.ogg"))
#explosao_som = pygame.mixer.Sound(os.path.join("assets","sound","explosao.wav"))
#musica = pygame.mixer.Sound(os.path.join("assets","sound","ledzepelin.mp3"))
#musica.play(loops=-1)


loop = True
relogio = pygame.time.Clock()
while loop:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            loop = False
      
        if event.type == pygame.MOUSEBUTTONDOWN and pode_disparar:
            print(tempo_disparo)
            laser_rec = lasersurf.get_rect(midbottom=navRec.midtop)
            laser_list.append(laser_rec)
            
            #calculo do tempo para um novo disparo
            pode_disparar = False
            tempo_disparo = pygame.time.get_ticks()
            #Executa som do laser
           # laser_som.play()
           
        if event.type == meteoro_tempo:
            x_pos = randint(-110, width+110)
            y_pos = randint(-100, -50)
            metoro_rec = meteor_img.get_rect(center=(x_pos,y_pos))
            # Criando uma direção para os metoros    
            direcao = pygame.math.Vector2(uniform(-0.5,0.5),1)
            metoros_list.append((metoro_rec,direcao))

    #Limitando os frames  (FPS)
    relogio.tick(120)
    #Limitando os frames  (FPS)
    dt = relogio.tick(120)/1000

    # entrada do mouse    
    navRec.center = pygame.mouse.get_pos()
    # Atualizando os Quadros
    display.fill('black')
    display.blit(bg1, bgR1) 


    #campo mouse
   # capRec.center = pygame.mouse.get_pos()
    #campo
    #display.fill('black')
    #display.blit(cg1, cgR1)    

    #utilizando o retangulo para poscionar a nave
    display.blit(nave, navRec)

    #campo
    #display.blit(campo, capRec)

    #display.blit(texto, (10,10))
    displayScore(display=display,font=font)
    #Lista de Lasers e tempo entre o laser
    laser_update(laser_list)  
    pode_disparar = laser_timer(pode_disparar,duracao=500)
    print(pode_disparar)
    #Lista de Meteoros
    meteoro_update(meteoro_list=metoros_list)



    #Criando colisão meteoro e a nave
    for meteoro_tupla in metoros_list:
        rec_meteoro = meteoro_tupla[0]
        if navRec.colliderect(rec_meteoro):
            pygame.quit()
            sys.exit()
    
    for laser_ret in laser_list:
        for meteoro_tupla in metoros_list:
            if laser_ret.colliderect(meteoro_tupla[0]):
                metoros_list.remove(meteoro_tupla)
                laser_list.remove(laser_ret)
                #explosao_som.play()


    for rec in laser_list:
        display.blit(lasersurf,rec)  

    for rec in metoros_list:
        display.blit(meteor_img,rec[0]) 

    #Criando colisão campo
    for meteoro_tupla in metoros_list:
        rec_meteoro = meteoro_tupla[0]



           


    pygame.display.update()

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.tela = pygame.display.set_mode((const.LARGURA, const.ALTURA))
        pygame.display.set_caption(const.TITULO)
        self.esta_rodando = True
        self.fonte =pygame.font.match_font(const.FONTE)
        self.car_arq()

    def car_arq(self):
        dir_imgs = os.path.join(os.getcwd(), 'imagens')
        self.tela = os.path.join(dir_imgs, 'tela.jpg')
        self.logo = os.path.join(dir_imgs, 'faixa1.png')
        self.logo = pygame.image.load(self.logo).convert()

    def most_text(self, texto, tam, cor, x, y):
        fonte = pygame.font.Font(self.fonte, tam)
        texto = fonte.render(texto, True, cor)
        texto_rect = texto.get_rect()
        texto_rect.midtop = (x,y)
        self.tela.blit(texto, texto_rect)

    def tel_star(self):
        self.most_texto('-Pressione qualquer tecla', 32, const.COR, const.LARGURA / 2, 320)
        pygame.display.flip()
        #esp_jog = esperar por jogador
        self.esp_jog()

    def esp_jog(self):
        esperando = True
        while esperando:
            self.relogio.tick(const.FPS)
            for event in pygame.event.get():
                if event.type ==pygame.QUIT:
                    esperando = False
                    self.esta_rodando = False
                if event.type == pygame.KEYUP:
                    esperando = False

g = Game()
g.tel_star()

while g.esta_rodando:
    g.novo_jogo()
    


pygame.quit()