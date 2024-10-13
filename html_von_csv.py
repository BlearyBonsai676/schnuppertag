import pandas as pd
import matplotlib.pyplot as plt
import webbrowser

# Lese CSV file
datei_pfad = r"C:\Users\rdmin\OneDrive\Dokumente\Platzierungen_Federer.csv"
daten = pd.read_csv(datei_pfad)

# Diagramm erstellen und speichern
plt.figure(figsize=(10, 6))
plt.plot(daten['Jahr'], daten['Platzierung'].fillna(0), marker='o', linestyle='-', color='b')
plt.title("Roger Federer's Weltranglistenpositionen")
plt.xlabel("Jahr")
plt.ylabel("Rang (1 = bester Rang)")
plt.gca().invert_yaxis()  # Invertiere die y-Achse, da 1 der beste Rang ist
plt.grid(True)
chart_datei_pfad = 'federer_ranking_chart.png'
plt.savefig(chart_datei_pfad)

# nur für den test
# plt.show()

#html- Datei erstellen und Tabelle + Grafik integrieren
html_datei_pfad = 'federer_ranking.html'
with open(html_datei_pfad,'w', encoding='utf-8') as html_datei:
    html_datei.write(f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Roger Federer's Rankings</title>
        <style>
            table {{
                width: 50%;
                margin: 20px auto;
                border-collapse: collapse;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
            }}
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            img {{
                display: block;
                margin: 20px auto;
            }}
        </style>
    </head>
    <body>
        <h1 style="text-align: center;">Roger Federer's Ranglistenpositionen</h1>
        <img src="{chart_datei_pfad}" alt="Federer's Ranking Chart">
        <table>
            <tr>
                <th>Jahr</th>
                <th>Rang</th>
            </tr>
    """)
    
    # Daten zur Tabelle hinzufügen
    for _, row in daten.iterrows():
        rank = row['Platzierung'] if pd.notna(row['Platzierung']) else 'Karriereende'
        html_datei.write(f"<tr><td>{int(row['Jahr'])}</td><td>{rank}</td></tr>")
    
    html_datei.write("""
      </table>
    </body>  
    </html>
    """)

# öffne html Datei im standart Browser
webbrowser.open(html_datei_pfad)