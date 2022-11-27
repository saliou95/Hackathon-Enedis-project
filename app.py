from flask import Flask, render_template, url_for, request
import pandas as pd
import os

app = Flask(__name__)


#insertion de l'image
IMG_FOLDER = os.path.join('static', 'images')

app.config['UPLOAD_FOLDER'] = IMG_FOLDER
Flask_Logo = os.path.join(app.config['UPLOAD_FOLDER'], 'enedis3.png')

conso_list =[]

def uploadCsv():
    input_file = "C:/Users/Saliou95/Desktop/Hackathon RESPONSE/Data/CDC par client/ACDC_CC_STM A 25_11_2022.csv"
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


    # print(data)
    conso_list = list(data["consomation"])
    heures_list = list(data["heure"])
    dates_list = list(data["date"].astype('str'))
    
    print(type(conso_list))
    # finalDataset=[]
    # finalDataset.append(conso_list, dates_list)
    return conso_list, dates_list
    # fileJson = data.to_json("clean_file.json")



@app.route('/', methods=['GET', 'POST'])
def home():
    conso_list, dates_list=uploadCsv()
    req_result = False
    if request.method == 'POST':
        form = request.form
        req_result = data(form)
    return render_template('pages/home.html', datas = req_result, conso = conso_list, dates=dates_list, user_image=Flask_Logo)


def data(form):
    hce = request.form['hce']
    Hparams = int(request.form['Hparams'])
    qt_int = int(request.form['qt'])
 
#   qt_seconds = qt_int / 1000 
#   rr_interval = (6000 / heart_rate) 
#   QTc = qt_seconds / math.sqrt(rr_interval) 
#   formated_QTc = round((QTc * 1000) * 10, 0)
#   if (formated_QTc > 440 and sex == 'm') or (formated_QTc > 460 and sex == 'f'):
#     prolonged = True
#   else:
#     prolonged = False
    return ""


@app.route('/about')
def about():
    return render_template('pages/about.html', user_image=Flask_Logo)

@app.route('/contact')
def contact():
    return render_template('pages/contact.html', user_image=Flask_Logo)



@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', user_image=Flask_Logo), 404



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5080)