# Ce programme extrait les données du sites spoticar.fr afin d'y recupérer les voitures dispo.
# Made by Djemel in 2023
# mail : bcbdjemel@gmail.com
# github : https://github.com/BEN-Djemel
# ------------------------------------------------------------------------------------------------
# importation des modules
import pandas as pd
import csv
import requests
from IPython.display import display
from bs4 import BeautifulSoup

url = 'https://www.spoticar.fr/voitures-occasion' 
maPage = requests.get(url).text; # recuperer le code de la page avec requests
soup = BeautifulSoup(maPage, "html.parser")
mesBoites=soup.find(["div"], class_="row grid-range gtm-list-vo-items") # La page principale avec les voitures
test = mesBoites.contents

# Je créer une fonction pour rendre plus beau mon code.
# Elle me servira à recuperer une image parmis plusieurs Images disponible.
tousLesImages=[]
def mesImg(k):
    global tousLesImages
    # On va faire une boucle pour recuperer une image parmis 4 
    mesImages360=test[k].find_all('img')
    for vv in mesImages360 :
        tousLesImages.append(vv['data-src'])
    return tousLesImages

# Je vais maintenant stocker mes données dans differentes variables pour plus tard en avoir une dataframe
listes_Voitures=[]
j=1
while j < 24 : # Si on veut retirer une voiture, on doit retirer -2 à la boucle.
    nouvellesListes_Voitures={}
        # La fonction strip() verifie si il y a « \ n » (retour chariot) en tant que string dans une string.
    imgVoiture = mesImg(j)[0]
    nomVoiture = test[j].find(["span"], class_="title").text.strip()
    motorisation = test[j].find(["span"], class_="sub-title vo-version-one-line").text.strip()
    spec = test[j].find(["ul"], class_="tags").text.strip().split('\n')
    prix = test[j].find(["p"], class_="price").text.strip()
    nouvellesListes_Voitures['image de la voiture']=imgVoiture
    nouvellesListes_Voitures['nom de la voiture']=nomVoiture
    nouvellesListes_Voitures['motorisations']=motorisation
    nouvellesListes_Voitures['compteur']=spec[0]
    nouvellesListes_Voitures['carburant']=spec[1]
    nouvellesListes_Voitures['premiere mise en circulation']=spec[2]
    nouvellesListes_Voitures['boite']=spec[3]
    nouvellesListes_Voitures['prix']=prix
    listes_Voitures.append(nouvellesListes_Voitures)
    j+=2 # on recupere une voiture toutes les deux valeurs donc on augmente j de +2

# Conversion en dataframe
dfVoitures=pd.DataFrame(listes_Voitures, columns=['image de la voiture','nom de la voiture','motorisations','compteur','carburant','premiere mise en circulation','boite','prix'])
display(dfVoitures)

# convertir en fichier csv
dfVoitures.to_csv('voituresOccasionsBySpoticar.csv', index=False, sep='\t', encoding='utf-8-sig')
"""
with open('voituresOccasionsBySpoticar.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerow(dfVoitures)
"""