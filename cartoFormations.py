# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 18:52:54 2016

@author: Mathias Brenet
"""
import pandas as panda #module de  lecture 
import folium #Module de cartographie
import pickle #pour importer la corespondance coord/ville

registre=open('dicoPosit.txt', 'rb')
dicoPaysVilleCoord=pickle.load(registre) #charge la corrspondance ville/ccordonnées
carte = folium.Map(location=[46.52, 2.1959],zoom_start=7) #genere la carte 

def getCoord(ville, pays) : #fonction donnant la corespondance ville lat/long
   liste=[dicoPaysVilleCoord[pays][ville][1],dicoPaysVilleCoord[pays][ville][0]]
   return liste

def ajouterPoint(ville,pays, taille, tag, couleur): #fonction ajoutant un point sur une carte
    carte.circle_marker(location=getCoord(ville, pays), radius=taille,
                    popup=tag, line_color=couleur,
                    fill_color=couleur)
                    
def creerLien(url, nom):
    lien="<a href="+'"'+url+'"'+'target="_blank"> '+nom+"</a>" 
    return lien   
      
dicoFormationVille={}       
listeCouleurs=["#FE2E2E","#00FF40","#2E64FE"]  

tableau=panda.read_csv('formations.csv', sep="\t", header=None, names=["ville", "formation", "url","typeFormation"])
n=tableau["ville"].count()
for x in range(0,n): #itere sur chaque ligne du fichier
    ville=tableau["ville"][x]
    formation=tableau["formation"][x]
    url=tableau["url"][x]
    typeFormation=tableau["typeFormation"][x]
    if dicoFormationVille.has_key(ville): # ajoute la formation
        if typeFormation =="Master":
            dicoFormationVille[ville][0].append([formation, url])
        if typeFormation =="Licence":
            dicoFormationVille[ville][1].append([formation, url])
        if typeFormation =="DUT":
            dicoFormationVille[ville][2].append([formation, url])
    else:
        dicoFormationVille[ville]=[[],[],[]]# genere les listes et ajoute la formation
        if typeFormation =="Master":
            dicoFormationVille[ville][0].append([formation, url])
        if typeFormation =="Licence":
            dicoFormationVille[ville][1].append([formation, url])
        if typeFormation =="DUT":
            dicoFormationVille[ville][2].append([formation, url])
  
for ville in dicoFormationVille:
    m=len(dicoFormationVille[ville][0])+len(dicoFormationVille[ville][1])+len(dicoFormationVille[ville][2])
    # m nombre total de formations
    for i in range(0,3): # itere sur les 3 types de formations
        n=len(dicoFormationVille[ville][i])
        #n nombre de formations d'un seul type
        if n>0:
            tag="<b>"+ville+" ("+str(m)+")" 
            #genere l'etiquette
            if i==0:
                tag=tag+" Master"+" : </b>"+"<br>"
            elif i==1:
                tag=tag+" Licence"+" : </b>"+"<br>"
            elif i==2:
                tag=tag+" DUT"+" : </b>"+"<br>"
            for formations in dicoFormationVille[ville][i]:
                lien=creerLien(formations[1],formations[0])
                tag=tag+lien+"<br>" #ajoute la formation et va à la ligne
            if i==0:
                if n==1:
                    n=2 # si il n'a qu'un master le cercle est un peu plus grand pour eviter les superpositions
                ajouterPoint(ville, "FR", 6000*n,tag,listeCouleurs[i])
            if i!=0:
                ajouterPoint(ville, "FR", 5000*n,tag,listeCouleurs[i])
        
carte.create_map(path='CarteFormations.html')  
