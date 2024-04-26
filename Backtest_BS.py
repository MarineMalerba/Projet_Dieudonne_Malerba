import numpy as np
import scipy.stats as sp
import pandas as pd
import yfinance as yf
from matplotlib import pyplot as plt 


#Liste des symboles des actions
table=pd.read_excel("./Projet.xlsx")
symbols=table.iloc[:,0].tolist() #Extrait toutes les lignes de la première colonne et transforme ce tableau en liste


#Début et fin de la période pour laquelle on souhaite avoir les données de chaque action
start_date = pd.Timestamp.now() - pd.DateOffset(months=6)
end_date = pd.Timestamp.now()


#Récupération des données historiques pour chaque action dans un dictionnaire
historical_data = {} #Clé: symbole de l'entreprise, Valeur: cours de l'action

for symbol in symbols:
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    historical_data[symbol] = stock_data

#Fixation de la valeur de la volatilité implicite 
sigma=0.20

#Taux sans risque r : taux LIBOR 3 mois
r=0.0559129

#Choix de t : période de 3 mois
t=90/365

norm_table = np.random.normal(0, 1, 100) #Array de nombres aléatoires générés selon une distribution normale centrée réduite
aide=0
difference=0

for symbol in historical_data:
    j=0

    for i, row in stock_data.iterrows() :
        j+=1

        if j>int(len(stock_data)/2):
            break

        #Calcul du cours du sous-jacent à la date t par Black-Scholes
        UA_t=0

        for norm in norm_table:
            UA_t = UA_t+ (row.iloc[4] * np.exp((r - 0.5 * sigma ** 2) * t + sigma * np.sqrt(t) * norm))

        UA_t /= len(norm_table)

        #Récupération de cours du sous-jacent à la date t (Close)
        real_UA_t= stock_data.iloc[j+int(len(stock_data)/2),4]

        difference += 1 - UA_t/real_UA_t #Comparaison et stockage de la différence (en pourcentage)
        aide+=1

print(difference/aide)
