#!/usr/bin/env python

from threading import Thread
import serial
import time
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import csv
import copy

'''
Programmation Objet
Classe qui va fournir les données pour les tracés
'''

class CapteurDonneesArduino:
    # Constructeur de la classe
    def __init__(self, portSerie = '/dev/cu.usbmodem14101', vitessePort = 38400,
                 nombrePointsGraphes = 100, nombreOctetsParDonnee = 2, nombreVoies = 2):
        self.portSerie = portSerie                              # Nom du port auquel se connecter
        self.vitessePort = vitessePort                          # Vitesse de transmission sur le port
        self.nombrePointsGraphes = nombrePointsGraphes          # Nombre de points de la fenêtre de tracé
        self.nombreVoies = nombreVoies                          # Nombre de voies (de canaux) à traiter
        self.NombreOctetsParDonnee = nombreOctetsParDonnee      # Nombre d'octets pour un point de données
        self.donneesLues = bytearray(nombreVoies * nombreOctetsParDonnee)   # Pour stocker les données à chaque lecture sur le port série
        self.listeDonnees=[]                                    # Tableau qui va contenir deux tableaux FIFO
        # FIFO (deque) pour le stockage de ce qui va venir de A0 et qui doit être affiché
        self.listeDonnees.append(collections.deque([0] * nombrePointsGraphes, maxlen=nombrePointsGraphes))
        # FIFO (deque) pour le stockage de ce qui va venir de A1 et qui doit être affiché
        self.listeDonnees.append(collections.deque([0] * nombrePointsGraphes, maxlen=nombrePointsGraphes))
        self.arretDemande = False                               # La fermeture du programme a été demandée
        self.receptionEnCours = False                           # La réception de données est en cours
        self.processusLectureDonnees = None                     # Contient le processus chargé de lire les données
        self.donneesCsv = [[],[]]                               # Tableau contenant toutes les données acquises

        print('Connexion en cours à: ' + str(portSerie) + ' à la vitesse de  ' + str(vitessePort) + ' bits/s.')
        try:
            # Création de la connexion série
            self.connexionSerie = serial.Serial(portSerie, vitessePort, timeout=4)
            print('Connecté à ' + str(portSerie) + ' à ' + str(vitessePort) + ' bits/s.')
        except:
            print("Impossible de se connecter à " + str(portSerie) + ' à ' + str(vitessePort) + ' bits/s.')

    # Lance la lecture sur le port série
    # Retourne à l'appelant quand la lecture a effectivement commencé
    def lireDonneesSeries(self):
        if self.processusLectureDonnees == None:                                 # Si le processus n'a pas été créé
            self.processusLectureDonnees = Thread(target=self.creerProcessusLectureDonnees())  # On le crée
            self.processusLectureDonnees.start()                                 # On le lance
            while self.receptionEnCours != True:                # On attend avant de retourner à l'appelant
                time.sleep(0.1)                                 # Tant qu'on ne reçoit rien

    # Recoit en paramètre les tracés matplot et met à jour leurs données pour l'animation
    def alimenterDonneesAnimation(self, frame, lines):
        for i in range(self.nombreVoies):
            lines[i].set_data(range(self.nombrePointsGraphes), self.listeDonnees[i])

    # Constructeur du thread de lecture des données série
    def creerProcessusLectureDonnees(self):
        time.sleep(1.0)                                     # Pause de une seconde pour que le transfert commence
        self.connexionSerie.reset_input_buffer()            # On vide le buffer pour être sûr d'avoir un A0 et un A1 ensuite
        while (not self.arretDemande):                      # Tant que la fermeture du programme n'est pas demandée
            self.connexionSerie.readinto(self.donneesLues)  # Lecture de 2 valeurs, donc 4 octets
            self.receptionEnCours = True                    # On stocke l'information que le transfert a commencé
            if len(self.donneesLues)>0:                             # Si on a bien lu quelque chose (2 valeurs)
                donneesCopiees = copy.deepcopy(self.donneesLues[:])    # On fait une copie locale de ces données
                for i in range(2):                              # Boucle pour stocker A0 et A1 dans les bonnes collections
                    # on prend les éléments 2 par 2, chaque greoupe de 2 octets correspondant à une donnée de point
                    donneePoint = donneesCopiees[(i*self.NombreOctetsParDonnee):(self.NombreOctetsParDonnee + i*self.NombreOctetsParDonnee)]
                    # Reconstitution d'un entier à partir des deux octets qui ont été lus
                    value,  = struct.unpack('h', donneePoint)
                    # Stockage dans les tableaux lus par les procédures d'affichage
                    self.listeDonnees[i].append(value)
                    # Stockage dans le tableau global d'acquisition
                    self.donneesCsv[i].append(value)

    # Appelé lors de la fermeture de l'application
    # Pour se déconnecter du port série
    def close(self):
        self.arretDemande = True              # Va de fait indiquer au processus de lecture qu'il peut s'arrêter
        self.processusLectureDonnees.join()   # Attend que le processus thread finisse l'exécution
        self.connexionSerie.close()       # Fermeture de la connexion série
        print('Déconnecté...Ecriture des fichiers csv')
        for i in range(self.nombreVoies):
            wtr = csv.writer(open ('out7_' + str (i) + '.csv', 'w'), delimiter=',', lineterminator='\n')
            for x in self.donneesCsv[i]:
                wtr.writerow([x])


# Création d'une fonction qui constitue le programme
def run():
    # Nom du port Série (ici sur Mac)
    portSerie = '/dev/cu.usbmodem14101'
    # Vitesse de transmission - bits/s - doit être en phase avec la carte
    vitessePort = 38400
    # Nombre maximal de points dans l'animation
    nombrePointsGraphe = 2000
    # Nombre d'octets représentant un point de données (ici deux octets - entier)
    nombreOctetsParDonnee = 2        # number of bytes of 1 data point
    nombreVoies = 2                  # On lit A0 et A1
    # Création de la connexion avec le port série sur lequel est branché la carte arduino
    capteur = CapteurDonneesArduino(portSerie, vitessePort, nombrePointsGraphe, nombreOctetsParDonnee, nombreVoies)
    # Commencement de la lecture sur le port série (par fil d'exécution indépendant)
    # Ce thread alimente les variables de l'objet "sensor"
    capteur.lireDonneesSeries()

    # Exploitation des données du sensor pour afficher en temps réel
    pltInterval = 50                    # Période de mise à jour du tracé (50 Hz, inutile au dessus)
    xmin = 0
    xmax = nombrePointsGraphe
    ymin = 0                            # 0 = 0V, 1024 = 5V
    ymax = 1024
    # Création de la figure
    fig = plt.figure(figsize=(10, 8))
    # Ajout des axes à la fiugure
    ax = plt.axes(xlim=(xmin, xmax), ylim=(ymin, ymax))
    ax.set_title('Signaux A0 et A1')                    # Titre
    ax.set_xlabel("Temps")                              # Label axe X
    ax.set_ylabel("Sorties A0 et A1 (V)")               # Label Axe Y
    lineLabel = ['Signal Traité', 'Signal brut']        # Légende des courbes
    style = ['r-', 'c-']                                # Styles de ligne pour les deux tracés
    lines = []                                          # Tableau des tracés de lignes
    for i in range(nombreVoies):                                  # Ajout des deux tracés de ligne au tableau
        # Axes.plot renvoie une liste de lignes représentant les tracés effectués => ici un seul par appel, d'où [0]
        lines.append( ax.plot([], [], style[i], label=lineLabel[i])[0])
    # Lancement de l'animation : le second argument est la fonction à appeler pour mettre à jour le 3e argument
    # fargs doit absolument etre un tuple
    anim = animation.FuncAnimation(fig, capteur.alimenterDonneesAnimation, fargs=(lines,), interval=pltInterval)
    plt.legend(loc="upper left")                        # Positionnement de la légende
    plt.show(block=True)                                # Ne pas retourner avant fermeture
    capteur.close()                                      # Fermeture du capteur

# Lancement du programme
run()
