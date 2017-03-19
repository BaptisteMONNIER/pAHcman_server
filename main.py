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

        self.rect.center = [SCREEN_WIDTH/2,SCREEN_HEIGHT/2]
        self.orientation = 'w'


    """
    Methode mettant à jour la position du sprite
    Paramètres :
        - keys : touches enfoncée
    """
    def update(self,keys,murs):

        mur = self.rect.collidelist(murs)

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
        self.rect = self.rect.move([-10,0])

    """
    Methode gérant le déplacement vers la droite
    """
    def moveRight(self):
        self.orientation = 'e'
        self.rect = self.rect.move([10,0])

    """
    Methode gérant le déplacement vers le haut
    """
    def moveUp(self):
        if 'e' in self.orientation:
            self.orientation = 'ne'
        elif 'w' in self.orientation:
            self.orientation = 'nw'
        self.rect = self.rect.move([0,-10])

    """
    Methode gérant le déplacement vers le haut
    """
    def moveDown(self):
        if 'e' in self.orientation:
            self.orientation = 'se'
        elif 'w' in self.orientation:
            self.orientation = 'sw'

        self.rect = self.rect.move([0,10])

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

    def create_murs(self):
        self.murs = []

        #Haut de la map
        self.murs.append(Mur(0,0,SCREEN_WIDTH,15))

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


        #Interieur de la map
        self.murs.append(Mur(88,88,15,15))
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
        self.denis.update(data['keystrokes'],self.murs)

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
        channel.create_murs()
        print('client connecté')

        if len(self.clients) == 1:
            for client in self.clients:
                client.Send({'action':'start'})
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
        for client in self.clients:
            if client.denis.rect.collidelist(client.murs) == -1:
                client.Send({'action':'denis','denis':[client.denis.rect.centerx,client.denis.rect.centery,client.denis.orientation]})

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
