import pandas as pd
import os

input_file = "Hackathon_RESPONSE/CDC par client/ACDC_CC_STM A 25_11_2022.csv"

file = open(input_file,"r")



lines = file.readlines()
dates = []
heures = []
conss = []

#verifier si les consommations sont par 5 minutes ou bien par 10 minutes

line1 = lines[1].replace("\n","").split(" ")
date1 = line1[0]
heure_cons1 = line1[1].split(";")
heure1 = ":".join(heure_cons1[0].split(":")[:2])
min1 = int(heure1.split(":")[1])


line2 = lines[2].replace("\n","").split(" ")
date2 = line2[0]
heure_cons2 = line2[1].split(";")
heure2 = ":".join(heure_cons2[0].split(":")[:2])
min2 = int(heure1.split(":")[1])

by_10 = False

#si les deux premiers valeurs de consomation sont multiple de 10 alors le fichier peut contenir des durées de 10 minutes et de 5 minutes
if ((min1 % 10)== 0) and ((min2 % 10)  == 0):
    by_10 = True


if by_10 :
    for i in range(1,len(lines)):

        line = lines[i].replace("\n","").split(" ")
        date = line[0]
        heure_cons = line[1].split(";")
        heure = ":".join(heure_cons[0].split(":")[:2])
        min = int(heure.split(":")[1])
        cons = heure_cons[1]
        cons = float(cons.replace(",","."))

        if (min % 10) == 5 :
            conss[-1] += cons
            conss[-1] = conss[-1]/2
        else :
            dates.append(date)
            heures.append(heure)
            conss.append(cons)
else:
    for i in range(1, len(lines)):

        line = lines[i].replace("\n", "").split(" ")
        date = line[0]
        heure_cons = line[1].split(";")
        heure = ":".join(heure_cons[0].split(":")[:2])
        min = int(heure.split(":")[1])
        cons = heure_cons[1]
        cons = float(cons.replace(",", "."))


        dates.append(date)
        heures.append(heure)
        conss.append(cons)

data = pd.DataFrame(data = {"date":dates,"heure":heures,"consomation":conss})
data["date"] = pd.to_datetime(data["date"])
#data["heure"] = pd.to_datetime(data["heure"],format='%H:%M')
data["consomation"] = data["consomation"].astype("float")
#format='%H:%M

data.to_csv("clean_file.csv",index=False)