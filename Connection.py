from pymongo import MongoClient
import pandas as pd
import numpy as np

import json
class Connection():


    def __init__(self):
        login = ''

        password = ''  # J'avais changé le mot de passe pendant mes test, c'est le nouveau mot de passe.
        host = 'cluster0.kwhckqe.mongodb.net'
        db = 'UserData'
        uri = f'mongodb+srv://{login}:{password}@{host}/{db}?retryWrites=true&w=majority'
        client = MongoClient(uri)
        self.db = client['UserData']

    def charge_data(self):
        electricite_collection = self.db['Electricite_data_final']
        data = electricite_collection.find({})

        date = []
        heure = []
        consomation = []
        for document in data:
            try:
                # print(document)
                consomation.append(document['consommation'])
                date.append(document['date'])
                heure.append(document['heures'])

            except:
                pass

        self.df = pd.DataFrame(data={'date': date, 'consommation': consomation})

        self.df.date = pd.to_datetime(self.df['date'], dayfirst=True)
        # df.set_index(df.date,inplace=True)


    def data_by_day(self):
        electricite_collection = self.db['Electricite_data_final']
        data = electricite_collection.find({})

        date = []
        heure = []
        consomation = []
        for document in data:
            try:
                # print(document)
                consomation.append(document['consommation'])
                date.append(document['date'])
                heure.append(document['heures'])

            except:
                pass

        self.df_day =  pd.DataFrame(data={'date':date,'heure':heure , 'consommation':consomation})
        self.df_day['heure'] = self.df_day['heure'].apply(lambda x: x + ':00')
        self.df_day['heure'] = pd.to_datetime(self.df_day['heure'].values)
        self.df_day['heure'] = self.df_day['heure'].dt.hour
        self.df_day = self.df_day.groupby(by=['date', 'heure']).mean()

        dic = dict()

        index = self.df_day.index
        cons = self.df_day.consommation.values

        for i in range(len(index)):
            if index[i][0] not in dic:
                dic[index[i][0]] = dict()
                dic[index[i][0]]['heure'] = list()
                dic[index[i][0]]['consomation'] = list()

            dic[index[i][0]]['heure'].append(str(index[i][1]))
            dic[index[i][0]]['consomation'].append(str(cons[i]))


        #with open('data.json', 'w') as fp:
        #    json.dump(dic, fp)

        return dic



    def data_by_year(self):
        self.df_year =  self.df.groupby(self.df.date.dt.year).mean()

    def data_by_month(self,year_1,year_2):
        self.df_month = self.df[((self.df.date > year_1) & (self.df.date < year_2))]

        self.df_month = self.df_month.groupby(self.df_month.date.dt.month).mean()

    def data_by_year_month(self,year,month):
        self.df_year_month = self.df[(self.df.date.dt.year == year) & (self.df.date.dt.month == month)]
        self.df_year_month = self.df_year_month.groupby(self.df_year_month.date.dt.day).mean()


    def create_semester_data(self):
        df_sem = self.df.groupby(self.df.date).mean()

        spring_19 = df_sem[(df_sem.index >= '2019-04-02') & (df_sem.index <= '2019-06-20') ].sum()[0]
        summer_19 = df_sem[(df_sem.index >= '2019-06-21') & (df_sem.index <= '2019-09-20') ].sum()[0]
        autumn_19 = df_sem[(df_sem.index >= '2019-09-21') & (df_sem.index <= '2019-12-20') ].sum()[0]
        winter_19 = df_sem[(df_sem.index >= '2019-12-21') & (df_sem.index <= '2019-12-31') ].sum()[0]

        spring_20 = df_sem[(df_sem.index >= '2020-03-21') & (df_sem.index <= '2020-06-20')].sum()[0]
        summer_20 = df_sem[(df_sem.index >= '2020-06-21') & (df_sem.index <= '2020-09-20')].sum()[0]
        autumn_20 = df_sem[(df_sem.index >= '2020-09-21') & (df_sem.index <= '2020-12-20')].sum()[0]
        winter_20 = df_sem[((df_sem.index >= '2020-12-21') & (df_sem.index <= '2020-12-31') ) |
                           ((df_sem.index >= '2020-01-01') & (df_sem.index <= '2020-03-20'))
                           ].sum()[0]

        spring_21 = df_sem[(df_sem.index >= '2021-03-21') & (df_sem.index <= '2021-06-20')].sum()[0]
        summer_21 = df_sem[(df_sem.index >= '2021-06-21') & (df_sem.index <= '2021-09-20')].sum()[0]
        autumn_21 = df_sem[(df_sem.index >= '2021-09-21') & (df_sem.index <= '2021-12-20')].sum()[0]
        winter_21 = df_sem[((df_sem.index >= '2021-12-21') & (df_sem.index <= '2021-12-31')) |
                           ((df_sem.index >= '2021-01-01') & (df_sem.index <= '2021-03-20'))
                           ].sum()[0]
        spring_22 = df_sem[(df_sem.index >= '2022-03-21') & (df_sem.index <= '2022-06-20')].sum()[0]
        summer_22 = df_sem[(df_sem.index >= '2022-06-21') & (df_sem.index <= '2022-09-20')].sum()[0]
        autumn_22 = df_sem[(df_sem.index >= '2022-09-21') & (df_sem.index <= '2022-12-20')].sum()[0]
        winter_22 = df_sem[((df_sem.index >= '2022-12-21') & (df_sem.index <= '2022-12-31')) |
                           ((df_sem.index >= '2022-01-01') & (df_sem.index <= '2022-03-20'))
                           ].sum()[0]

        dic = {
            '2019' : {'labels':  ['Printemps','Ete','Automne','Hiver'] , 'data':[spring_19,summer_19,autumn_19,winter_19]},
            '2020': {'labels': ['Printemps', 'Ete', 'Automne', 'Hiver'],
                     'data': [spring_20, summer_20, autumn_20, winter_20]},
            '2021': {'labels': ['Printemps', 'Ete', 'Automne', 'Hiver'],
                     'data': [spring_21, summer_21, autumn_21, winter_21]},
            '2022': {'labels': ['Printemps', 'Ete', 'Automne', 'Hiver'],
                     'data': [spring_22, summer_22, autumn_22, winter_22]}

        }
        #with open('data_semestre.json', 'w') as fp:
        #    json.dump(dic, fp)

        return dic
    def skip_null(self, tmp,ind, rng=12):
        cons_by_month= []

        j = 0
        for i in range(rng):
            if i + 1 in ind:
                cons_by_month.append(str(tmp[j]))
                j += 1
            else:
                cons_by_month.append("N/A")

        cons_by_month = list(cons_by_month)
        return cons_by_month