# VibrationGui

## Objectifs

L’objectif de ce développement est de faire une interface 
graphique PC avec le module Arduino mesurant les vibrations
dans les moteurs de drone.

Il y a donc une première partie de communication série avec l’appareil.
Une seconde partie sera dédiée au traitement des données de mesures.

# Dépendances

Ce projet est conçu pour fonctionner avec python 3.8 (testé avec python 3.8
sous linux et 3.9 sous windows).
Il dépend de plusieurs librairies externes :

 * numpy : pour l’algèbre linéaire et l’analyse de données.
 * matplotlib : pour tracer des courbes.
 * pygubu (et pygubu designer) : outils pour simplifier l’utilisation de tkinter.
 * pyserial : pour communiquer avec l’outil de mesure

En outre, ce programme nécessite l’installation de tcl/tk pour le bon fonctionnement 
de tkinter. (sous windows, tout est installé avec python, sous linux il peut 
être nécessaire d’installer le package tcl/tk séparément)

## Modules

### Communication série

lorem ipsum

### Interface Graphique

lorem ipsum

### Traitement des données

lorem ipsum
