import pandas as pd
import time
from subprocess import Popen

# Lese CSV file

datei_pfad = r"C:\Users\rdmin\OneDrive\Dokumente\Platzierungen_Federer.csv"
daten = pd.read_csv(datei_pfad)

# Berechnung

beste_platzierung = daten['Platzierung'].min()
schlechteste_platzierung = daten['Platzierung'].max()
durchschnitt_platzierung = daten['Platzierung'].mean()

# Ausgabe

print("Die beste Platzierung von Federer war: ",beste_platzierung)
time.sleep(0.5)
print(f"Die schlechteste Platzierung von Federer war: {schlechteste_platzierung}")
time.sleep(0.5)
print(f"Die Durchschnittsplatzierung von Federer war: {durchschnitt_platzierung:.2f}")

p = Popen(datei_pfad, shell = True)