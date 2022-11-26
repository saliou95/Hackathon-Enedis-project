import pandas as pd

def get_outlier(df_in, col_name):
    q1 = df_in[col_name].quantile(0.25)
    q3 = df_in[col_name].quantile(0.75)
    iqr = q3-q1 #Interquartile range

    seuil = q3+1.5*iqr

    return seuil

input_file = "Hackathon_RESPONSE/clean_data/ACDC_CC_STM A 25_11_2022.csv"

data = pd.read_csv(input_file)
print(get_outlier(data, 'consomation'))
