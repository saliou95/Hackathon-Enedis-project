import pandas as pd
import os


file_input_path = "Hackathon_RESPONSE/CDC par client/ACDC_CC_STM A 25_11_2022.csv"
file_output_path = "Hackathon_RESPONSE/clean_data/ACDC_CC_STM A 25_11_2022.csv"
file = open(file_input_path,"r")

lines = file.readlines()
dates = []
heures = []
conss = []



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

data = pd.DataFrame(data = {"date":dates,"heure":heures,"consomation":conss})
data["date"] = pd.to_datetime(data["date"])
#data["heure"] = pd.to_datetime(data["heure"],format='%H:%M')
data["consomation"] = data["consomation"].astype("float")
#format='%H:%M

data.to_csv(file_output_path,index=False)



