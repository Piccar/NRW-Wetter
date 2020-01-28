#The MIT License (MIT)
#
#Copyright (c) 2019 Frederic
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
#Importiern von notwendigen Bibliotheken
import urllib.request
import os
import matplotlib.pyplot as plt
import csv
#Vordefinieren von Variablen
pathabsolut="void"
temp='https://www.lanuv.nrw.de/fileadmin/lanuv/luft/temes/T_AM1H.csv'
winddirec='https://www.lanuv.nrw.de/fileadmin/lanuv/luft/temes/WR_VM1H.csv'
windspeed='https://www.lanuv.nrw.de/fileadmin/lanuv/luft/temes/WG_SM1H.csv'
#Einführen des Nutzers in das Programm
print('Wetterdaten als Grafische Darstellung \n \n') 
print('Dieses Programm dieht zur Grafischen aufarbeitung Tagesaktueller Wetterdaten.')
print('Bitte bestätigen Sie Ihre Eingaben immer mit der ENTER-Taste.')
print('Stellen Sie sicher dass Sie eine Stabile Internet Verbinung haben um die Datensätze herrunterladen zukönnen.\n\n')
#Vorbereiten der downlaods der Datensätze
print("Bitte gebe den absoluten Speicherpfad für die Datein an. Dieses sollte ein Ordner sein.")
print(r"e.g. C:\Users\MaxMustermann\Desktop\ ")
while os.path.isdir(pathabsolut)== False:
    pathabsolut = input() #Abfrage ob der Speicherpfad valide ist
print("Beginne nun mit dem Download!")
print("Je nach Internetgeschwindigkeit kann es unterschiedlich lange dauern")
#Download der CSV-Datei und speichern des Pfades
print("Download 1 von 3")
temp, http = urllib.request.urlretrieve(temp,pathabsolut+'temperatur.csv')
print("Done")

print("Beginne Download 2 von 3")
winddirec, http =urllib.request.urlretrieve(winddirec,pathabsolut+'windrichtung.csv')
print("Done")

print("Beginne Download 3 von 3")
windspeed, http = urllib.request.urlretrieve(windspeed,pathabsolut+'windgesch.csv')
print("Done")

print("Die Daten wurden hier gespeichert",temp,winddirec,windspeed)
#Abfrage nach der Art des Datensatzes
print("\n Was soll dargestellt werden?")
print("1: Tempertatur")
print("2: Windrichtung")
print("3: Windgeschwindigkeit")
#Speichern des Pfades des Datensatzes und definition des Labels für matplotlib
while os.path.isfile(pathabsolut) == False:
    i=input("Bitte die Nummer eingeben: ")
    if i=="1":
        pathabsolut=temp
        label="Temperatur in °C"
    if i=="2":
        pathabsolut=winddirec
        label="Windrichtung in Grad"
    if i=="3":
        pathabsolut=windspeed
        label="Windgeschwindigkeit in Bft"

print("Lese Daten aus "+pathabsolut)
#Abfrage wie viele Tage angezeigt werden sollen
print("\n\nWie viele Tage sollen angezeigt werden?")
tage=int(input("Bitte in ganzen Tagen angeben: "))
tage = (tage*24) #Die Tage werden mit 24 multiplitziert da der Datensatz die
#Werte stündlich gespeichert hat

#Speichern der einzelnen Daten in ein Array
with open(pathabsolut) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    #Die Daten werden durch ein Simikolon getrennt des wegen wird es als 
    #Trennzeichen angegeben    
    next(csv_file)
    next(csv_file)
    #Die ersten beiden Zeilen werden nicht gebraucht und übersprungen
    data = []
    time = []
    date = []
    y=0
    #Erstellen von leeren Arrays    
    for line in csv_reader:
        y=y-1
        #Speichern der Daten
        data.append(line[2])
        #Speichern der Zeit. Alle 24h mit dem Datum
        if line[1] == str("24:00"):
            time.append(line[0])
        else:
            #Speichern der restlichen Stellen mit dem Iterator
            #Bei gleichen Werten funktioniert Matplot nicht richtig.
            time.append(y)

#Invertieren der Daten da der Datesatz von altem zu neustem Sortiert ist
time = time[::-1]
data = data[::-1]
#Eingrenzen der Daten mit dem angegebenen Wert
time = time[0:tage]
data = data[0:tage]

#Damit Matplot funktioniert müssen die Werte als Float vorliegen
#Floats benutzen jedoch Punkte als Komma. Im zuge dessen werden die Punkte durch Kommas ersetzt
#Leere werte werden als nan deklariert
values = []
for i in range(len(data)):
	if not data[i]: 
		data[i] = 'nan' 
	values.append(float(data[i].replace(',','.')))



#Auswahl der Speicherform des Graphen
print("\n\nDaten vorbereitet. Sollen diese als PNG oder SVG gespeichert werden?")
print("1: PNG")
print("2: SVG")
print("Alles andere: Nicht speichern")
i = int(input("Bitte die Nummer eingeben: "))

#Graphen definieren
plt.plot(time, values)
plt.xlabel("Zeit in Stunden")
plt.ylabel(label)
pathabsolut="void"  
plt.xticks(time[0::24])#Einstellen das nur die Ganzen Tage angezeigt werden
#sonst wird der Graph zu unübersichtlich


#Speichern des Graphen
if i == 1 or i == 2:
    while os.path.isdir(pathabsolut)== False:
        pathabsolut=input("Bitte gebe den absoluten Speicherpfad für die Datein an:")
if i == 1:
    plt.savefig(pathabsolut+"plot.png", format="png")
if i == 2:
    plt.savefig(pathabsolut+"plot.svg", format="svg")
#Plotten des Graphen
plt.show()
