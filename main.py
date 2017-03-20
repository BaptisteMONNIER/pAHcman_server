#!/usr/bin/python2
# -*- coding: utf-8 -*-

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

"""
Serveur du jeu pAHcman
"""

import sys, pygame
import os
from pygame.locals import *
import random
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
import time,sys
import traceback

"""
Charge une image png
Paramètres :
    - path : chemin de l'image
Retourne
    - image de type pygame.image
"""
def load_png(path):
        fullpath=os.path.join('.',path)
        try:
            image=pygame.image.load(fullpath)
            if image.get_alpha is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
        except pygame.error:
            print('Cannot load image: %s' % path)
            print(traceback.format_exc())
            raise SystemExit
        return image,image.get_rect()



"""
Classe gérant le sprite Mur
Hérite de :
    - pygame.sprite.Sprite
"""
class Mur(pygame.sprite.Sprite):
    """
    Constructeur de la classe Sprite
    """
    def __init__(self,x,y,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w,h),0,None)
        self.rect = pygame.Rect(x,y,w,h)


class AhBleu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image,self.rect=load_png("pics/ah.png")
        self.rect.center = [SCREEN_WIDTH/2,SCREEN_HEIGHT/2]
        self.direction = 'n'
        self.stop = False

    def update(self, keys, murs, denis):
        mur = self.rect.collidelist(murs)

        if(self.rect.colliderect(denis.rect)):
            self.stop = True
        else:
            self.stop = False

        if(self.rect.x < 0-self.rect.w):
            self.rect.x = SCREEN_WIDTH
        if(self.rect.x > SCREEN_WIDTH):
            self.rect.x = 0

        if mur == -1 or mur == 25:

            if keys[K_LEFT]:
                self.direction = 'w'
                self.rect = self.rect.move([-5,0])
            elif keys[K_RIGHT]:
                self.direction = 'e'
                self.rect = self.rect.move([5,0])
            elif keys[K_UP]:
                self.direction = 'n'
                self.rect = self.rect.move([0,-5])
            elif keys[K_DOWN]:
                self.direction = 's'
                self.rect = self.rect.move([0,5])

        else:


            if self.direction == 'w' :

                self.rect = pygame.Rect(murs[mur].rect.right,self.rect.y,self.rect.w,self.rect.h)

            elif self.direction == 'e':
                self.rect = pygame.Rect(murs[mur].rect.left-self.rect.w,self.rect.y,self.rect.w,self.rect.h)

            elif self.direction == 'n':

                self.rect = pygame.Rect(self.rect.x,murs[mur].rect.bottom,self.rect.w,self.rect.h)

            elif self.direction == 's':

                self.rect = pygame.Rect(self.rect.x,murs[mur].rect.top-self.rect.h,self.rect.w,self.rect.h)

"""
Classe gérant le sprite Denis
Hérite de :
    -  pygame.sprite.Sprite
"""
class Denis(pygame.sprite.Sprite):
    """
    Constructeur de la classe Denis
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image,self.rect=load_png("pics/denis/denis-w.png")

        self.image_e,_=load_png("pics/denis/denis-e.png")
        self.image_w,_=load_png("pics/denis/denis-w.png")
        self.image_ne,_=load_png("pics/denis/denis-ne.png")
        self.image_nw,_=load_png("pics/denis/denis-nw.png")
        self.image_se,_=load_png("pics/denis/denis-se.png")
        self.image_sw,_=load_png("pics/denis/denis-sw.png")

        self.rect.center = [SCREEN_WIDTH/2,SCREEN_HEIGHT/2+150]
        self.orientation = 'w'
        self.stop = False


    """
    Methode mettant à jour la position du sprite
    Paramètres :
        - keys : touches enfoncée
    """
    def update(self,keys,murs,ah):

        mur = self.rect.collidelist(murs)

        if(self.rect.colliderect(ah.rect)):
            self.stop = True
        else:
            self.stop = False

        if(self.rect.x < 0-self.rect.w):
            self.rect.x = SCREEN_WIDTH
        if(self.rect.x > SCREEN_WIDTH):
            self.rect.x = 0

        if mur == -1:

            if keys[K_LEFT]:
                self.moveLeft()
            elif keys[K_RIGHT]:
                self.moveRight()
            elif keys[K_UP]:
                self.moveUp()
            elif keys[K_DOWN]:
                self.moveDown()

        else:



            if self.orientation == 'w' :

                self.rect = pygame.Rect(murs[mur].rect.right,self.rect.y,self.rect.w,self.rect.h)

            elif self.orientation == 'e':
                self.rect = pygame.Rect(murs[mur].rect.left-self.rect.w,self.rect.y,self.rect.w,self.rect.h)

            elif 'n' in self.orientation:

                self.rect = pygame.Rect(self.rect.x,murs[mur].rect.bottom,self.rect.w,self.rect.h)

            elif 's' in self.orientation:

                self.rect = pygame.Rect(self.rect.x,murs[mur].rect.top-self.rect.h,self.rect.w,self.rect.h)

    """
    Methode gérant le déplacement vers la gauche
    """
    def moveLeft(self):
        self.orientation = 'w'
        self.rect = self.rect.move([-5,0])

    """
    Methode gérant le déplacement vers la droite
    """
    def moveRight(self):
        self.orientation = 'e'
        self.rect = self.rect.move([5,0])

    """
    Methode gérant le déplacement vers le haut
    """
    def moveUp(self):
        if 'e' in self.orientation:
            self.orientation = 'ne'
        elif 'w' in self.orientation:
            self.orientation = 'nw'
        self.rect = self.rect.move([0,-5])

    """
    Methode gérant le déplacement vers le haut
    """
    def moveDown(self):
        if 'e' in self.orientation:
            self.orientation = 'se'
        elif 'w' in self.orientation:
            self.orientation = 'sw'

        self.rect = self.rect.move([0,5])

"""
Classe ClientChannel, représentant un client
Hérite de:
    - Channel
"""
class ClientChannel(Channel):
    """
    Constructeur de la classe
    """
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)

    """
    Methode gérant le sprite contrôlé par un client en particulier
    Parametres : #TODO (à mettre en conformité dans le code)
        - number : numero du client
    """
    def create_denis(self):
        self.denis = Denis()

    def create_AhBleu(self):
        self.ahBleu = AhBleu()

    def create_murs(self):
        self.murs = []

        #Haut de la map
        self.murs.append(Mur(0,0,SCREEN_WIDTH,15))
        self.murs.append(Mur(SCREEN_WIDTH/2-5,15,10,100))

        #Côté gauche de la map
        self.murs.append(Mur(0,15,15,170))
        self.murs.append(Mur(0,185,200,15))
        self.murs.append(Mur(200,185,15,80))
        self.murs.append(Mur(0,265,215,15))
        self.murs.append(Mur(0,390,215,15))
        self.murs.append(Mur(200,405,15,80))
        self.murs.append(Mur(0,470,215,15))
        self.murs.append(Mur(0,470,15,SCREEN_HEIGHT-433))

        #Bas de la map
        self.murs.append(Mur(0,SCREEN_HEIGHT-15,SCREEN_WIDTH,15))

        #Côté droit de la map
        self.murs.append(Mur(SCREEN_WIDTH-15,15,15,170))
        self.murs.append(Mur(SCREEN_WIDTH-200,185,200,15))
        self.murs.append(Mur(SCREEN_WIDTH-215,185,15,80))
        self.murs.append(Mur(SCREEN_WIDTH-215,265,215,15))
        self.murs.append(Mur(SCREEN_WIDTH-215,390,215,15))
        self.murs.append(Mur(SCREEN_WIDTH-215,405,15,80))
        self.murs.append(Mur(SCREEN_WIDTH-215,470,215,15))
        self.murs.append(Mur(SCREEN_WIDTH-15,470,15,SCREEN_HEIGHT-433))


        #Interieur de la map, partie haute
        self.murs.append(Mur(88,88,100,15))
        self.murs.append(Mur(300,88,130,15))
        self.murs.append(Mur(SCREEN_WIDTH-188,88,100,15))
        self.murs.append(Mur(SCREEN_WIDTH-430,88,130,15))

        #cage à AH
        self.murs.append(Mur(SCREEN_WIDTH/2-150,SCREEN_HEIGHT/2-70,100,15))
        self.murs.append(Mur(SCREEN_WIDTH/2+50,SCREEN_HEIGHT/2-70,100,15))
        self.murs.append(Mur(SCREEN_WIDTH/2-50,SCREEN_HEIGHT/2-70,100,10))
        self.murs.append(Mur(SCREEN_WIDTH/2-150,SCREEN_HEIGHT/2+70,300,15))
        self.murs.append(Mur(SCREEN_WIDTH/2-150,SCREEN_HEIGHT/2-55,15,130))
        self.murs.append(Mur(SCREEN_WIDTH/2+135,SCREEN_HEIGHT/2-55,15,130))

        #partie entre la cage à AH et le haut de la map
        self.murs.append(Mur(288,185,1,100))
        self.murs.append(Mur(288,235,150,1))
        self.murs.append(Mur(SCREEN_WIDTH-287,185,1,100))
        self.murs.append(Mur(SCREEN_WIDTH-437,235,150,1))

        #barres entre la cage à AH et les côtés de la map
        self.murs.append(Mur(288,400,1,100))
        self.murs.append(Mur(SCREEN_WIDTH-287,400,1,100))

        #partie intérieure basse de la map
        self.murs.append(Mur(88,SCREEN_HEIGHT-103,300,15))
        self.murs.append(Mur(SCREEN_WIDTH-388,SCREEN_HEIGHT-103,300,15))
        self.murs.append(Mur(288,SCREEN_HEIGHT-153,15,50))
        self.murs.append(Mur(SCREEN_WIDTH-303,SCREEN_HEIGHT-153,15,50))
        self.murs.append(Mur(SCREEN_WIDTH/2-5,SCREEN_HEIGHT-178,10,90))
        self.murs.append(Mur(SCREEN_WIDTH/2-110,SCREEN_HEIGHT-193,220,15))
        self.murs.append(Mur(88,570,127,15))
        self.murs.append(Mur(SCREEN_WIDTH-215,570,127,15))

    """
    Méthode gérant la fermeture de la connexion côté client
    """
    def Close(self):
        self._server.del_client(self)

    """
    Méthode réceptionnant les touches enfoncée côté client
    Parametres:
        - data : message
    """
    def Network_keys(self, data):
        if(data['perso'] == 'denis'):
            self.denis.update(data['keystrokes'],self.murs,self.ahBleu)
        else:
            self.ahBleu.update(data['keystrokes'],self.murs,self.denis)

"""
Classe MyServer, réprésantant le serveur
Hérite de :
    - Server
"""
class MyServer(Server):
    channelClass = ClientChannel

    """
    Constructeur de la classe
    """
    def __init__(self,*args,**kwargs):
        Server.__init__(self,*args,**kwargs)
        self.clients = []
        self.run = False
        pygame.init()
        self.screen = pygame.display.set_mode((128,128))
        print('Serveur lauched')

    """
    Methode gérant la connexion d'un client au Serveur
    """
    def Connected(self,channel,addr):
        self.clients.append(channel)
        channel.create_denis()
        channel.create_AhBleu()
        channel.create_murs()
        print('client connecté')

        if len(self.clients) == 2:
            self.clients[0].Send({'action':'start','perso':'denis'})
            self.clients[1].Send({'action':'start','perso':'ah'})
            self.run = True

    """
    Methode gérant la deconnexion d'un client
    """

    def del_client(self,channel):
        print('client déconnecté')
        self.clients.remove(channel)

    """
    Methode renvoyant le résultat de l'évenement au client
    """
    def send_denis(self):
        if(len(self.clients) == 2):

            denis = self.clients[0].denis
            ah = self.clients[1].ahBleu

            for client in self.clients:
                if denis.rect.collidelist(client.murs) == -1:
                    client.Send({'action':'denis','denis':[denis.rect.centerx,denis.rect.centery,denis.orientation]})
                if ah.rect.collidelist(client.murs) == -1 or ah.rect.collidelist(client.murs) == 25:
                    client.Send({'action':'AhBleu','AhBleu':[ah.rect.centerx,ah.rect.centery]})

                if denis.stop or ah.stop:
                    client.Send({'action':'stop'})
    """
    Methode du jeu
    """
    def launch_game(self):
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            self.Pump()

            if self.run:
                self.send_denis()

"""
Programme principal du serveur
"""

if __name__ == '__main__':

    myServer = MyServer(localaddr = (sys.argv[1],int(sys.argv[2])))
    myServer.launch_game()
