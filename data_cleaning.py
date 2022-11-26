import pandas as pd
import os

for file_name in os.listdir("Hackathon_RESPONSE/CDC par client"):
    print(file_name)
    file = open("Hackathon_RESPONSE/CDC par client/"+file_name,"r")

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
        else :
            dates.append(date)
            heures.append(heure)
            conss.append(cons)

    data = pd.DataFrame(data = {"date":dates,"heure":heures,"consomation":conss})
    data["date"] = pd.to_datetime(data["date"])
    #data["heure"] = pd.to_datetime(data["heure"],format='%H:%M')
    data["consomation"] = data["consomation"].astype("float")
    #format='%H:%M

    data.to_csv("Hackathon_RESPONSE/clean_data/"+file_name,index=False)



