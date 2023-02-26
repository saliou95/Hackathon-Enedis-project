from flask import Flask, render_template, url_for, request
import pandas as pd
import os
from Connection import Connection
import json
import numpy as np
from dateutil import rrule
import datetime
import pickle
import statsmodels.api as sm
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_cors import cross_origin


app = Flask(__name__)
CORS(app)

api = Api(app)


#insertion de l'image
IMG_FOLDER = os.path.join('static', 'images')

app.config['UPLOAD_FOLDER'] = IMG_FOLDER
Flask_Logo = os.path.join(app.config['UPLOAD_FOLDER'], 'enedis3.png')


Connex  = Connection()
Connex.charge_data()
dic_day = Connex.data_by_day()

dic_ann =dict()
dic_y_m = dict()
dic_sem = dict()


@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def home():


    Connex.data_by_month('2019', '2020')
    cons_by_month_2019 = Connex.skip_null(Connex.df_month.values.reshape(-1) , Connex.df_month.index)

    Connex.data_by_month('2020', '2021')
    cons_by_month_2020 = Connex.skip_null(Connex.df_month.values.reshape(-1) , Connex.df_month.index)
    Connex.data_by_month('2021', '2022')
    cons_by_month_2021 = Connex.skip_null(Connex.df_month.values.reshape(-1), Connex.df_month.index)
    Connex.data_by_month('2022','2023')
    cons_by_month_2022 = Connex.skip_null(Connex.df_month.values.reshape(-1) , Connex.df_month.index)

    dic_ann['2019'] = {'data' :  cons_by_month_2019}
    dic_ann['2020'] = {'data' :  cons_by_month_2020}
    dic_ann['2021'] = {'data' :  cons_by_month_2021}
    dic_ann['2022'] = {'data' :  cons_by_month_2022}

    #with open('data_ann.json', 'w') as fp:
    #   json.dump(dic_ann, fp)




    month = 4
    year = 2019

    while (year < 2023) :
        try :
            print(month)
            Connex.data_by_year_month(year,month)
            rs = Connex.skip_null( list(Connex.df_year_month.values.reshape(-1)) , Connex.df_year_month.index , Connex.df_year_month.index[-1])
            labels = []
            for j in range(Connex.df_year_month.index[-1]):
                labels.append(j+1)

            if month < 10:
                mth ='0'+ str(month)
            else:
                mth = str(month)
            dic_y_m[str(year) + '-' + mth] = {}
            dic_y_m[str(year) + '-' + mth]['data'] = rs
            dic_y_m[str(year) + '-' + mth]['label'] = labels.copy()
            print(dic_y_m[str(year)+'-'+mth])

        except:
            pass
        month+=1
        if month >12 :
            month = 1
            year +=1

    #with open('data_y_m.json', 'w') as fp:
    #    json.dump(dic_y_m, fp)


    #prevision sur les deux prochaines jours
    # with open('arma.pkl','rb') as f:
    #    model =  pickle.load(f)

    model = sm.load('arma_s.pkl')
    prd = model.predict(698,699)

    last_day_pr = float(dic_y_m['2022-12']['data'][-1])

    jr1_prevision = int(last_day_pr + prd.values[0]*last_day_pr/100)
    jr2_prevision = int(jr1_prevision + prd.values[1]*jr1_prevision/100)
    global dic_sem
    dic_sem = Connex.create_semester_data()
    print("semmm",dic_sem)

    return render_template('pages/home.html',jr1_prv=jr1_prevision,jr2_prv=jr2_prevision, user_image=Flask_Logo)



@app.route('/about')
def about():
    return render_template('pages/about.html', user_image=Flask_Logo)

@app.route('/contact')
def contact():
    return render_template('pages/contact.html', user_image=Flask_Logo)




class by_year_month(Resource):
    def get(self,y_m):
        return   dic_y_m[y_m]

api.add_resource(by_year_month, '/cons_y_m/<string:y_m>')

class by_year(Resource):
    def get(self,y):
        return  dic_ann[y]

api.add_resource(by_year, '/cons_y/<string:y>')

class by_day(Resource):
    def get(self,day):
        return dic_day[day]

api.add_resource(by_day, '/cons_day/<string:day>')

class by_sem(Resource):
    def get(self,sem):
        return dic_sem[sem]

api.add_resource(by_sem, '/cons_sem/<string:sem>')




@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', user_image=Flask_Logo), 404



if __name__ == '__main__':
    app.run(debug=True)