import sys
import pygame
import random
from pygame.sprite import Sprite
from pygame.sprite import Group

""" Alexandre Norcia Medeiros 10295583
    Danilo Leonssio Alves 10408390
"""

class Configuracoes():
    """ Classe para guardar variaveis de configuracoes """
    def __init__(self):
        """ Inicializa com valores padroes """
        # Parametros da tela
        self.tela_inicial = pygame.image.load('imagens/tela_inicial.png')
        self.tela_game_over = pygame.image.load('imagens/game_over.png')
        self.tela_pause = pygame.image.load('imagens/pause.png')
        self.seletor = pygame.image.load('imagens/seletor.png')
        self.background = pygame.image.load('imagens/background.png')
        self.tela_x = 1205 # 1205 x 590  ou wide?
        self.tela_y = 590
        # Parametros da Nave ( PLAYER )
        self.img_nave = pygame.image.load('imagens/nave.png')
        self.img_nave_danificada = pygame.image.load('imagens/nave_danificada.png')
        self.img_nave_morta = pygame.image.load('imagens/nave_morta.png')
        # Parametros dos coracoes que representam as vidas do player
        # Mto importante que ambas imagens tenham mesma dimensao WxH
        self.img_coracao_cheio = pygame.image.load('imagens/coracao_cheio.png')
        self.img_coracao_vazio = pygame.image.load('imagens/coracao_vazio.png')
        # Parametros do tiro (e gerenciador)
        self.img_tiro = pygame.image.load('imagens/tiro1.png')
        self.img_tiro_inimigo = pygame.image.load('imagens/tiro1_inimigo.png')
        # Parametros dos inimigos (e gerenciador)
        self.img_inimigo_qtd = 3
        self.img_inimigos = []
        self.img_inimigos.append( pygame.image.load('imagens/inimigo1.png') )
        self.img_inimigos.append( pygame.image.load('imagens/inimigo2.png') )
        self.img_inimigos.append( pygame.image.load('imagens/inimigo3.png') )
        self.img_inimigo_morto = pygame.image.load('imagens/inimigo_morto.png')
        # Parametros dos items
        self.qtd_items = 4
        self.img_items = []
        self.img_items.append( pygame.image.load('imagens/item1.png') )
        self.img_items.append( pygame.image.load('imagens/item2.png') )
        self.img_items.append( pygame.image.load('imagens/item3.png') )
        self.img_items.append( pygame.image.load('imagens/item4.png') )
        # Items especiais
        self.img_arnold = pygame.image.load('imagens/arnold.png')
        self.cooldown_arnold = 1000
        # Parametros da pontuacao
        self.cor_pts = (242, 136, 45)
        self.tam_pts = 40 # tamanho da fonte
        self.tam_pts_game_over = 120 # tamanho da fonte no game over
        self.fonte_pts = None # nome da fonte (None -> padrao da pygame)

        self.reset()

    def reset(self):
        """ Reseta valores que sao possivelmente alterados pelo jogo """
        # nave
        self.vel_nave = 8 # velocidade
        self.vida_nave = 3 # Obs: comeca a contar do 1
        self.cooldown_dano = 300 # tempo ivuneralvel
        self.cooldown_tiro_nave = 400 # tempo entre tiros
        # tiro
        self.vel_tiro = 15 # velocidade do tiro
        self.dmg_tiro = 1 # dano
        self.vel_tiro_inimigo = 6 # velocidade do tiro
        self.dmg_tiro_inimigo = 1 # dano
        # inimigo
        self.img_inimigo_indice = 0
        self.vel_inimigo = 4 # velocidade
        self.vida_inimigo = 1
        self.cooldown_inimigo = 200 # tempo entre inimigos
        self.cooldown_inimigo_morte = 250 # tempo do inimigo morto
        self.cooldown_tiro_inimigo = 2000 # tempo entre tiros inimigos
        # Parametros dos items
        self.item_vida = 1 # adiciona x vidas
        self.item_cooldown_tiro = -50 # aumenta o rate dos tiros da nave
        self.item_vel_tiro = 2 # aumenta a velocidade dos tiros
        self.item_dmg_tiro = 1 # adiciona x de dano
        # Parametros da ondas de inimigos
        self.cooldown_onda = 8000 # tempo entre ondas de inimigos
        self.qtd_inimigos_onda = 5 # qtd de inimigos por onda
        # Parametros da pontuacao
        self.pts = 0
        self.add_pts_inimigo = 100 # qtd de pontos por inimigo morto
        # Parametros da dificuldade
        self.passo_dif = 400 # qtd de pontos para aumentar a dificuldade
        self.extra_dif = 3 # a cada x acresimos, acresenta dificuldades extras (ex: vida inimigo)
        self.add_vel_inimigo = 1 # acresimo na velocidade dos inimigos
        self.add_vel_tiro_inimigo = 2 # acresimo na velocidade do tiro inimigo
        self.add_cooldown_tiro_inimigo = -100 # (de)acresimo no tempo entre tiros dos inimigos
        self.add_cooldown_onda = -400 # (de)acresimo no tempo entre ondas
        # Parametros de dificuldade que nao acontecem tao frequentemente
        self.add_vida_inimigo = 1 # acresimo na vida dos inimigos
        self.add_qtd_inimigos = 1 # acresimo na qtd de inimigos por onda
        # Parametros limitadores de dificuldade/bonus
        self.min_cooldown_tiro_nave = 50
        self.min_cooldown_tiro_inimigo = 200
        self.min_cooldown_onda = 2000
        self.max_vel_tiro = 35
        self.max_vel_tiro_inimigo = 25
        self.max_vel_inimigo = 12

class Item(Sprite):
    """ Classe para representar 1 item """
    def __init__(self, tela, cfg, x, y, tipo):
        """ Inicializa o item a partir da posicao do player"""
        super(Item, self).__init__() # chama construtor da classe mae
        #guarda uma referencia da tela para desenhar
        self.tela = tela
        # atributos gerais
        self.img = cfg.img_items[ tipo ]
        self.tipo = tipo
        # atributos da posicao
        self.rect = self.img.get_rect() # get_rect() retorna obj Rect da pygames
        if y < self.rect.height:
            y += self.rect.height
        self.rect.bottom = y
        self.rect.left = x

    def ativa(self, cfg, nave, g_inimigos, g_pontos):
        """ Metodo que ativa o item """
        if self.tipo == 0: # item de vida
            nave.add_vida()
        elif self.tipo == 1: # item que aumenta a velocidade dos tiros e o fire rate
            if cfg.cooldown_tiro_nave > cfg.min_cooldown_tiro_nave:
                cfg.cooldown_tiro_nave += cfg.item_cooldown_tiro
            if cfg.vel_tiro < cfg.max_vel_tiro:
                cfg.vel_tiro += cfg.item_vel_tiro
        elif self.tipo == 2: # item q aumenta o dano dos tiros
            cfg.dmg_tiro += cfg.item_dmg_tiro
        elif self.tipo == 3: # arnold, mata todo mundo
            self.chama_arnold(cfg)
            g_inimigos.mata_todos()
            g_pontos.alterou = False
            g_pontos.prepara_pts()

    def chama_arnold(self, cfg):
        """ Metodo que ativa o item especial do arnold schwarzenegger """
        tempo_inicial = pygame.time.get_ticks() # fica um tempo esperando
        tempo_atual = tempo_inicial
        while tempo_atual - tempo_inicial < cfg.cooldown_arnold:
            self.tela.blit(cfg.img_arnold, cfg.img_arnold.get_rect())
            pygame.display.flip() # desenha arnold na tela
            tempo_atual = pygame.time.get_ticks()

    def desenha(self):
        """ Metodo que desenha o item na tela """
        # blit -> metodo da pygame para desenhar retangulo com imagem
        self.tela.blit(self.img, self.rect)

class Gerenciador_pontos():
    """ Classe que gerencia a pontuacao do jogador """
    def __init__(self, tela, cfg):
        """ Inicializa de maneira correta o gerenciador de pontos """
        # referencia da tela para desenhar
        self.tela = tela
        self.rect_tela = tela.get_rect()
        # guarda uma referencia da cfg pq nela que vai estar guradado os pts
        # para os outros gerenciadores poderem alterar
        self.cfg = cfg
        # parametros da fonte
        self.cor = cfg.cor_pts
        self.fonte = pygame.font.SysFont(cfg.fonte_pts, cfg.tam_pts)
        self.prepara_pts()
        # parametro para atualizacao
        self.alterou = True
        # group de items que sao gerados de acordo com os pontos
        self.items = Group()

    def prepara_pts(self):
        """ Cria objeto da fonte renderizado """
        pts_str = str(self.cfg.pts) # transforma nro em string
        # render(text, antialias, color, background=None) -> Surface
        self.img_pts = self.fonte.render(pts_str, True, self.cor)
        self.rect = self.img_pts.get_rect()
        self.rect.right = self.rect_tela.right - 20
        self.rect.top = 10

    def update(self, nave, g_inimigos):
        """ Atualiza valores do jogo para ficar mais dificil de acordo com a
            pontuacao, gera items aleatorios para o player e os ativa
        """
        # se ja nao atualizou e esta na hora de atualizar
        if not self.alterou and self.cfg.pts % self.cfg.passo_dif == 0:
            self.alterou = True

            # gera item aleatorio a 60 pixels de distancia da nave
            tipo = random.randint(0, self.cfg.qtd_items - 1)
            y = random.randint(self.rect_tela.top, self.rect_tela.bottom) # y aleatorio
            x = nave.rect.right + 60
            if x > self.rect_tela.right:
                x -= 500
            novo_item = Item(self.tela, self.cfg, x, y, tipo)
            self.items.add(novo_item)

            # acresimo na velocidade dos inimigos
            if self.cfg.vel_inimigo < self.cfg.max_vel_inimigo:
                self.cfg.vel_inimigo += self.cfg.add_vel_inimigo
            # acresimo na velocidade do tiro inimigo
            if self.cfg.vel_tiro_inimigo < self.cfg.max_vel_tiro_inimigo:
                self.cfg.vel_tiro_inimigo += self.cfg.add_vel_tiro_inimigo
            # (de)acresimo no tempo entre tiros dos inimigos
            if self.cfg.cooldown_tiro_inimigo > self.cfg.min_cooldown_tiro_inimigo:
                self.cfg.cooldown_tiro_inimigo += self.cfg.add_cooldown_tiro_inimigo
            # (de)acresimo no tempo entre ondas
            if self.cfg.cooldown_onda > self.cfg.min_cooldown_onda:
                self.cfg.cooldown_onda += self.cfg.add_cooldown_onda

            # tenta atualizar dificuldades extra
            if self.cfg.pts % ( self.cfg.passo_dif * self.cfg.extra_dif) == 0:
                # acresimo na vida dos inimigos
                self.cfg.vida_inimigo += self.cfg.add_vida_inimigo
                # mudanca na imagem do inimigo
                self.cfg.img_inimigo_indice = (self.cfg.img_inimigo_indice + 1) % self.cfg.img_inimigo_qtd
                # acresimo na qtd de inimigos por onda
                self.cfg.qtd_inimigos_onda += self.cfg.add_qtd_inimigos

        # verifica colisao do item com a nave
        colisao = pygame.sprite.spritecollide(nave, self.items, True)
        for item in colisao:
            item.ativa(self.cfg, nave, g_inimigos, self)

    def game_over(self):
        """ Posiciona pontos para game over """
        # igual ao prepara_pts, mas posiciona em outro lugar com outro tamanho
        pts_str = str(self.cfg.pts)
        self.fonte = pygame.font.SysFont(self.cfg.fonte_pts, self.cfg.tam_pts_game_over)
        # render(text, antialias, color, background=None) -> Surface
        self.img_pts = self.fonte.render(pts_str, True, self.cor)
        self.rect = self.img_pts.get_rect()
        self.rect.left = 635
        self.rect.y = 230

    def desenha(self):
        """ Desenha pontos """
        for item in self.items:
            item.desenha()
        self.tela.blit(self.img_pts, self.rect)

class Inimigo(Sprite):
    """ Classe para representar 1 inimigo """
    def __init__(self, tela, cfg, y):
        """ Inicializa o inimigo """
        super(Inimigo, self).__init__() # chama construtor da classe mae
        #guarda uma referencia da tela para desenhar
        self.tela = tela
        self.rect_tela = tela.get_rect()
        # atributos gerais
        self.img = cfg.img_inimigos[ cfg.img_inimigo_indice ]
        self.img_morto = cfg.img_inimigo_morto
        self.vel = cfg.vel_inimigo
        self.vida = cfg.vida_inimigo
        self.morto = False
        # variaveis para manter imagem de morte
        self.cooldown_morte = cfg.cooldown_inimigo_morte
        self.cooldown_ultimo_hit = pygame.time.get_ticks()
        # atributos da posicao
        self.rect = self.img.get_rect() # get_rect() retorna obj Rect da pygames
        self.rect.right = self.rect_tela.right
        if self.rect.height > y: # para nao nascer fora da tela
            y = self.rect.height
        self.rect.bottom = y # altura passada por parametro no construtor

    def update(self):
        """ Metodo que atualiza o inimigo """
        self.rect.centerx -= self.vel # anda para esquerda

    def desenha(self):
        """ Metodo que desenha a nave na tela """
        # blit -> metodo da pygame para desenhar retangulo com imagem
        self.tela.blit(self.img, self.rect)

    def danifica(self, dano):
        """ Metodo que tira vida do inimigo e potencialmente o marca como morto"""
        self.vida -= dano
        self.cooldown_ultimo_hit = pygame.time.get_ticks()
        if self.vida <= 0: # troca imagem para inimigos mortos
            self.morto = True
            self.img = self.img_morto

    def mata(self):
        """ Metodo que mata o inimigo"""
        self.danifica(self.vida)

class Gerenciador_inimigos():
    """ Classe que gerencia diversos inimigos """
    def __init__(self, tela, cfg):
        """ Funcao inicializa gerenciador """
        # guarda uma referencia da tela para desenhar e cfg para criar tiros
        self.tela = tela
        self.cfg = cfg
        self.rect_tela = tela.get_rect()
        # Lista com inimigos ativos.
        self.inimigos = Group() #Groups eh uma classe container da pygames para lidar com sprites
        # atributos para lidar com o cooldown (tempo entre inimigos e tempo geral entre ondas)
        self.ultimo_inimigo = pygame.time.get_ticks()
        self.ultima_onda = pygame.time.get_ticks()
        self.qtd = cfg.qtd_inimigos_onda

    def update(self, g_tiros, g_pontos):
        """ metodo que gera inimigos """
        tempo_atual = pygame.time.get_ticks()
        # verifica se comecou onda
        if tempo_atual - self.ultima_onda >= self.cfg.cooldown_onda:
            self.ultima_onda = tempo_atual
            self.qtd = self.cfg.qtd_inimigos_onda # reseta qts inimigos vao ser criados
        # tenta criar um novo inimigo
        if self.qtd > 0 and tempo_atual - self.ultimo_inimigo >= self.cfg.cooldown_inimigo:
            self.ultimo_inimigo = tempo_atual
            y = random.randint(self.rect_tela.top, self.rect_tela.bottom)
            novo_inimigo = Inimigo(self.tela, self.cfg, y)
            self.inimigos.add(novo_inimigo)
            self.qtd -= 1

        # atualiza inimigos existentes
        self.inimigos.update() # metodo do Objeto Gruop que chama os .update de cada inimigo
        # tira do Group os inimigos que sairam da tela e que estao mortos
        for inimigo in self.inimigos.copy():
            if inimigo.rect.left <= 0 or (inimigo.vida <= 0
             and  tempo_atual - inimigo.cooldown_ultimo_hit >= self.cfg.cooldown_inimigo_morte):
                self.inimigos.remove(inimigo)

        # verifica colisao com tiros
        # funcao que recebe dois grupos e a opcao de matar
        # e retorna dicionario com colisoes {1 membro grupo1:[x membros grupo 2]}
        colisoes = pygame.sprite.groupcollide(self.inimigos, g_tiros.tiros, False, True)
        for colidido in colisoes.keys():
            dano = 0
            for tiro in colisoes[colidido]:
                dano += tiro.dmg
            if not colidido.morto: # so danifica se nao esta morto
                colidido.danifica(dano)
                if colidido.morto: # se morreu depois de danificar, aumenta os pts
                    self.cfg.pts += self.cfg.add_pts_inimigo
                    g_pontos.alterou = False
                    g_pontos.prepara_pts()

    def mata_todos(self):
        """ Metodo que mata todos inimigos vivos e pontua """
        for inimigo in self.inimigos:
            inimigo.mata()
            self.cfg.pts += self.cfg.add_pts_inimigo

    def desenha(self):
        """ Funcao que desenha os inimigos pertencentes ao Group na tela """
        for inimigo in self.inimigos:
                inimigo.desenha()

class Tiro(Sprite): # heranca de Sprite para funcionar com grupos
    """ Classe para representar 1 tiro """
    def __init__(self, tela, cfg, x, y, player):
        """ Inicializa o tiro a partir da posicao do player"""
        super(Tiro, self).__init__() # chama construtor da classe mae
        #guarda uma referencia da tela para desenhar
        self.tela = tela
        # atributos gerais
        if player:
            self.img = cfg.img_tiro
            self.vel = cfg.vel_tiro
            self.dmg = cfg.dmg_tiro
            self.sentido = 1
        else: # inimigo
            self.img = cfg.img_tiro_inimigo
            self.vel = cfg.vel_tiro_inimigo
            self.dmg = cfg.dmg_tiro_inimigo
            self.sentido = -1
        # atributos da posicao
        self.rect = self.img.get_rect() # get_rect() retorna obj Rect da pygames
        self.rect.centery = y
        self.rect.left = x

    def update(self):
        """ Metodo que atualiza o tiro """
        self.rect.centerx += self.vel * self.sentido

    def desenha(self):
        """ Metodo que desenha o tiro na tela """
        # blit -> metodo da pygame para desenhar retangulo com imagem
        self.tela.blit(self.img, self.rect)

class Gerenciador_tiros():
    """ Classe que gerencia diversos tiros """
    def __init__(self, tela, cfg):
        """ Funcao inicializa gerenciador """
        # guarda uma referencia da tela para desenhar e cfg para criar tiros
        self.tela = tela
        self.cfg = cfg
        self.rect_tela = tela.get_rect() # auxiliar
        # Lista com tiros ativos.
        self.tiros = Group() # Groups eh uma classe container da pygames para lidar com sprites
        self.tiros_inimigos = Group()
        # atributos para lidar com o cooldown (tempo entre tiros)
        self.atirando = False
        self.ultimo_tiro_nave = pygame.time.get_ticks()
        self.ultimo_tiro_inimigo = self.ultimo_tiro_nave

    def update(self, nave, g_inimigos):
        """ metodo que atualiza a posicao dos tiros e remove os que sairam da tela """
        # tenta criar um novo tiro
        tempo_atual = pygame.time.get_ticks()
        if self.atirando == True and tempo_atual - self.ultimo_tiro_nave >= self.cfg.cooldown_tiro_nave:
            self.ultimo_tiro_nave = tempo_atual
            x = nave.rect.right
            y = nave.rect.centery
            novo_tiro = Tiro(self.tela, self.cfg, x, y, True)
            self.tiros.add(novo_tiro)

        # tenta criar novo tiro dos inimigos
        if g_inimigos.inimigos and tempo_atual - self.ultimo_tiro_inimigo >= self.cfg.cooldown_tiro_inimigo:
            # se estiver no tempo e tiver inimigos vivos --> atira
            self.ultimo_tiro_inimigo = tempo_atual
            i = random.randint(0, len(g_inimigos.inimigos) - 1) # escolhe inimigo
            j = 0
            for inimigo in g_inimigos.inimigos: # acha x y do inimigo
                if j == i:
                    x = inimigo.rect.left
                    y = inimigo.rect.centery
                j += 1
            novo_tiro = Tiro(self.tela, self.cfg, x, y, False) # diz que e tiro de inimigo
            self.tiros_inimigos.add(novo_tiro)

        # atualiza tiros existentes
        self.tiros.update() # metodo do Objeto Gruop que chama os .update de cada tiro
        self.tiros_inimigos.update()
        # tira do Group os tiros que sairam da tela
        for tiro in self.tiros.copy():
            if tiro.rect.right >= self.rect_tela.right:
                self.tiros.remove(tiro)
        for tiro in self.tiros_inimigos.copy():
            if tiro.rect.right <= 0:
                self.tiros_inimigos.remove(tiro)

    def desenha(self):
        """ Funcao que desenha os tiros pertencentes ao Group na tela """
        for tiro in self.tiros: # desenha tiros da nave
            tiro.desenha()
        for tiro in self.tiros_inimigos: # desenha tiros dos inimigos
            tiro.desenha()

class Coracao(Sprite):
    """ Classe que um coracao na tela """
    def __init__(self, tela, cfg, offset):
        """ Funcao inicializa gerenciador """
        super(Coracao, self).__init__() # chama construtor da classe mae
        # referencia da tela para desenhar
        self.tela = tela
        # imagens
        self.img = cfg.img_coracao_cheio
        self.img_vivo = cfg.img_coracao_cheio
        self.img_morto = cfg.img_coracao_vazio
        # atributos da posicao
        self.rect = self.img.get_rect() # get_rect() retorna obj Rect da pygames
        self.rect.centery = self.rect.height + 3 # altura + 3 pixels do topo
        self.rect.centerx = (self.rect.width + 3) * (offset + 1)# distancia da tela e o N dele * seu tamanho + 3

    def update(self, vivo):
        """ Metodo que atualiza o inimigo """
        if vivo:
            self.img = self.img_vivo
        else:
            self.img = self.img_morto

    def desenha(self):
        """ Metodo que desenha o coracao na tela """
        # blit -> metodo da pygame para desenhar retangulo com imagem
        self.tela.blit(self.img, self.rect)

class Gerenciador_coracoes():
    """ Classe que representa um grupo de coracoes (vidas) """
    def __init__(self, tela, cfg):
        """ Funcao inicializa gerenciador """
        # referencias para criar novos coracoes
        self.tela = tela
        self.cfg = cfg
        # imagens
        self.coracao_cheio = cfg.img_coracao_cheio
        self.coracao_vazio = cfg.img_coracao_vazio
        # informacoes dos coracoes
        self.qtd = cfg.vida_nave
        self.qtd_vivos = cfg.vida_nave
        self.coracoes = Group() # Grupo para guardar coraceos

        # inicializa o grupo de maneira apropriada
        i = 0
        while i < self.qtd:
            novo_coracao = Coracao(self.tela, self.cfg, i)
            self.coracoes.add(novo_coracao)
            i += 1

    def update(self, nave):
        """ metodo que atualiza a imagem dos coracoes """
        if self.qtd < nave.vidas:
            self.qtd = nave.vidas
            novo_coracao = Coracao(self.tela, self.cfg, self.qtd - 1)
            self.coracoes.add(novo_coracao)

        self.qtd_vivos = nave.vidas
        i = 0
        for coracao in self.coracoes:
            if i < self.qtd_vivos:
                coracao.update(True) # vivo
            else:
                coracao.update(False) # morto
            i += 1

    def desenha(self):
        """ Funcao que desenha os coracoes pertencentes ao Group na tela """
        for coracao in self.coracoes:
                coracao.desenha()

class Nave(Sprite):
    """ Classe que representa o player """
    def __init__(self, tela, cfg):
        """ Cria a Nave espacial e a posiciona """
        super(Nave, self).__init__() # chama construtor da classe mae
        #guarda uma referencia da tela para desenhar e as configuracoes para velocidade.
        self.tela = tela
        #cria o retangulo com a imagem carregada
        self.img = cfg.img_nave
        self.img_normal = cfg.img_nave
        self.img_danificada = cfg.img_nave_danificada
        self.img_morta = cfg.img_nave_morta
        self.rect = self.img.get_rect() # get_rect() retorna obj Rect da pygames
        self.rect_tela = tela.get_rect() # usa para nao andar para fora da tela
        #coloca valores iniciais para os atributos de Rect, para ir no canto esq
        self.rect.centery = self.rect_tela.centery
        self.rect.left = self.rect_tela.left;
        #atributos para controlar a vida do player
        self.vidas = cfg.vida_nave
        self.coracoes = Gerenciador_coracoes(tela, cfg)
        self.ultimo_dano = pygame.time.get_ticks()
        self.cooldown_dano = cfg.cooldown_dano
        self.morta = False

        #atributos para controlar movimento
        self.vel = cfg.vel_nave
        self.moving_R = False
        self.moving_L = False
        self.moving_U = False
        self.moving_D = False

    def update(self, g_inimigos, g_tiros):
        """ Metodo que atualiza posicao da Nave """
        tempo_atual = pygame.time.get_ticks()

        # diversos ifs separados para poder andar em mais de uma direcao.
        # e verificacoes para nao sair da tela.
        if self.vidas > 0 and self.moving_R and self.rect.right < self.rect_tela.right:
            self.rect.centerx += self.vel
        if self.vidas > 0 and self.moving_L and self.rect.left > 0:
            self.rect.centerx -= self.vel
        if self.vidas > 0 and self.moving_U and self.rect.top > 0:
            self.rect.centery -= self.vel
        if self.vidas > 0 and self.moving_D and self.rect.bottom < self.rect_tela.bottom:
            self.rect.centery += self.vel

        # verifica colisao com inimigos e tiros inimigos
        # spritecollide(sprite, group, dokill, collided = None) -> Sprite_list
        colisao = pygame.sprite.spritecollide(self, g_inimigos.inimigos, True)
        colisao2 = pygame.sprite.spritecollide(self, g_tiros.tiros_inimigos, True)

        # se a lista de colisao contem algum elemento e a dif entre tempos e maior
        if (colisao or colisao2) and (tempo_atual - self.ultimo_dano >= self.cooldown_dano):
            leva_dano = False # assume que colidiu com um inimigo morto
            for inimigo in colisao:
                if inimigo.morto == False:
                    leva_dano = True # colidiu com um inimigo vivo
            if leva_dano or colisao2:
                dano = 0
                if colisao2:
                    for tiro in colisao2:
                        dano += tiro.dmg
                else:
                    dano = 1 # dano da colisao com inimigos
                self.vidas -= dano
                self.ultimo_dano = tempo_atual
                if self.vidas <= 0: # morre
                    self.img = self.img_morta
                else: # leva dano
                    self.img = self.img_danificada
        elif (tempo_atual - self.ultimo_dano >= self.cooldown_dano) and self.vidas > 0:
            self.img = self.img_normal

        if self.vidas <= 0 and (tempo_atual - self.ultimo_dano >= self.cooldown_dano):
            self.morta = True

        # Update dos coracoes
        self.coracoes.update(self)

    def add_vida(self):
        self.vidas += 1

    def desenha(self):
        """ Metodo que desenha a nave na tela """
        # blit -> metodo da pygame para desenhar retangulo com imagem
        self.tela.blit(self.img, self.rect)
        self.coracoes.desenha()

def pause(tela, cfg):
    """ Funcao que faz a tela de game over """
    # tela de pause
    tela.blit(cfg.tela_pause, cfg.tela_pause.get_rect())
    acabou = False
    while not acabou:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() # fecha jogo
            elif event.type == pygame.KEYDOWN: # espera apertar espaco
                if event.key == pygame.K_p: # acaba
                    acabou = True

def game_over(tela, cfg, g_pontos):
    """ Funcao que faz a tela de game over """
    # tela de game over
    tela.blit(cfg.tela_game_over, cfg.tela_game_over.get_rect())
    # desenha pontuacao
    g_pontos.game_over()
    g_pontos.desenha()
    acabou = False
    while not acabou:
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() # fecha jogo
            elif event.type == pygame.KEYDOWN: # espera apertar espaco
                if event.key == pygame.K_SPACE: # acaba
                    acabou = True

def game_loop(tela, cfg):
    """ Funcao que faz o loop principal do jogo (inimigos, tiros, etc) """
    nave = Nave(tela, cfg)
    g_tiros = Gerenciador_tiros(tela, cfg)
    g_inimigos = Gerenciador_inimigos(tela, cfg)
    g_pontos = Gerenciador_pontos(tela, cfg)
    background_rect = cfg.background.get_rect()

    while not nave.morta: # trocar para nao morto
        # verifica teclado e mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() # fecha jogo
            # teclado
            elif event.type == pygame.KEYDOWN: # apertou uma tecla
                # if elif pq so pode apertar um evento pode ser so uma tecla.
                # Movimento da Nave
                if event.key == pygame.K_RIGHT:
                    nave.moving_R = True
                elif event.key == pygame.K_LEFT:
                    nave.moving_L = True
                elif event.key == pygame.K_UP:
                    nave.moving_U = True
                elif event.key == pygame.K_DOWN:
                    nave.moving_D = True
                # Tiro
                elif event.key == pygame.K_SPACE:
                    g_tiros.atirando = True
                # Pause
                elif event.key == pygame.K_p:
                    pause(tela, cfg)
                    nave.moving_R = False # evitar bugs
                    nave.moving_L = False
                    nave.moving_U = False
                    nave.moving_D = False
                    g_tiros.atirando = False
            elif event.type == pygame.KEYUP: # solto uma tecla
                # Movimento da Nave
                if event.key == pygame.K_RIGHT:
                    nave.moving_R = False
                elif event.key == pygame.K_LEFT:
                    nave.moving_L = False
                elif event.key == pygame.K_UP:
                    nave.moving_U = False
                elif event.key == pygame.K_DOWN:
                    nave.moving_D = False
                # Tiro
                elif event.key == pygame.K_SPACE:
                    g_tiros.atirando = False

        # Update de objetos.
        nave.update(g_inimigos, g_tiros)
        g_tiros.update(nave, g_inimigos)
        g_inimigos.update(g_tiros, g_pontos)
        g_pontos.update(nave, g_inimigos)

        # Prepara para jogar na tela.
        tela.blit(cfg.background, background_rect)
        nave.desenha()
        g_tiros.desenha()
        g_inimigos.desenha()
        g_pontos.desenha()

        # Joga na tela as ultimas novidades
        pygame.display.flip()

    game_over(tela, cfg, g_pontos) # chama tela de game over

def start_game():
    """ Funcao que faz o loop da tela inicial do jogo (quit, start highscore etc) """
    pygame.init() # inicializa os modulos do pygame corretamente

    #objeto que guarda configuracoes padroes
    cfg = Configuracoes();
    # objeto que representa a tela
    tela = pygame.display.set_mode((cfg.tela_x, cfg.tela_y)) # ((,)) pq eh um pair
    pygame.display.set_caption("Batalha Espacial com Arnold Schwarzenegger") # nome da janela
    seletor_rect = cfg.seletor.get_rect()
    seletor_rect.x = 70 # hardcodado para tela inicial 1205 x 590
    seletor_rect.y = 360 # 295 365 415 original
    background_rect = cfg.background.get_rect()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() # fecha jogo
            elif event.type == pygame.KEYDOWN: # seleciona opcoes
                if event.key == pygame.K_UP and seletor_rect.y > 360:
                    seletor_rect.y -= 60
                elif event.key == pygame.K_DOWN and seletor_rect.y < 420:
                    seletor_rect.y += 60
                elif event.key == pygame.K_SPACE: # seleciona
                    if seletor_rect.y == 360: # esta em cima do play
                        cfg.reset()
                        game_loop(tela, cfg)
                    elif seletor_rect.y == 420: # esta em cima do quit
                        sys.exit() # fecha jogo

        # Desenha coisas
        tela.blit(cfg.tela_inicial, background_rect) # background
        tela.blit(cfg.seletor, seletor_rect) # x
        # Joga na tela as ultimas novidades
        pygame.display.flip()

# primeiro comando a ser executado de fato.
start_game()
