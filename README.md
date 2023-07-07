# Photoplethysmography
Ces scripts python ont été écrits dans le cadre de mon TIPE (travail individuel de recherche présenté au concours d'entrée dans les grandes écoles scientifiques)

## Traitement analogique et acquisition du signal
Il s'est agit de construire un montage électronique :
- à base de led / photoresistor permettant de produire un signal photopléthysmographique à partir d'une application sur un doigt par exemple
- à base d'amplis op, de condensateurs et de résistance, afin de filtrer (filtres passe-bas et passe-haut) et amplifier le signal produit

On obtenait alors un signal analogique de cardiogramme, numérisé via une carte arduino permettant l'aquisition numérique du signal analogique (une tension). Un programme python permet de capturer cette numérisation et d'enregistrer les différentes valeurs échantillonnées dans des fichiers CSV our affichage ou traitements futurs.

## Traitement numérique du signal brut.
Il s'est ensuite agi d'appliquer des traitements de filtres numériques au signal brut pour là encore, filtrer et amplifier celui-ci afin de retrouver le cardiogramme analogique

## Illustration du résultat
![Image cardiogramme](https://github.com/lcharles038/photoplethysmography/blob/main/cardiogramme.png?raw=true)

## Librairies utilisées
numpy - scipy - matplotlib

## Présentation complète
![Rendu TIPE](https://github.com/lcharles038/photoplethysmography/blob/main/cardiogramme.png?raw=true)
