# Importem les llibreries necessàries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import collections

# Web scrapping
r = requests.get('https://www.nme.com/photos/the-500-greatest-albums-of-all-time-100-1-1426116')

# Adaptació d'html
soup = BeautifulSoup(r.text, 'html.parser')
resultats = soup.find_all('span', attrs={'class': 'tdb-sml-description'})

# Proves per comprovar que s'extreia el resultat desitjat
# primer_resultat = resultats[0]
# print(primer_resultat)
# print(primer_resultat.find('p').contents[1].text)
# print(primer_resultat.find('p').contents[2].text[2:6])
# print(primer_resultat.find('p').contents[4].text)
# print(len(resultats))
# print(resultats[1])

# Selecció, neteja de dades i construcció del dataframe
diccionari = []
for resultat in resultats:
    try:
        any = resultat.find('p').contents[2].text[2:6]
        nom = resultat.find('p').contents[1].text
        descripcio = resultat.find('p').contents[4][1:]
        diccionari.append((any, nom, descripcio))
    except IndexError:
        pass

top = pd.DataFrame(diccionari, columns=['any', 'album', 'descripcio'])

# Gràfic de barres amb el nombre d'àlbums a la llista per any
anys = collections.Counter(top["any"])
plt.bar(range(len(anys)), list(anys.values()), align='center')
plt.xticks(range(len(anys)), list(anys.keys()))
plt.title("Anys amb més àlbums al top 100 històric")
plt.show()

# Exportem el dataframe a un csv
top.to_csv('top_100_albums.csv', index=False, encoding='utf-8')