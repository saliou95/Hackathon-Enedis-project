

def max_value(csv_path, hyperparemeter):
    
    import pandas as pd
    import numpy as np
    from scipy.signal import argrelextrema

    #convert csv into df 
    df = pd.read_csv(csv_path, sep = ",")
    
    #concate date + heure

    df["date"] = df["date"] + " " + df["heure"]
    
    # found local peaks 

    n = 500 # number of points to be checked before and after

    df['min'] = df.iloc[argrelextrema(df.consomation.values, np.less_equal,
                    order=n)[0]]['consomation']
    df['max'] = df.iloc[argrelextrema(df.consomation.values, np.greater_equal,
                    order=n)[0]]['consomation']

    max_value = 0

    for num in df["max"]:
        if (max_value is None or num > max_value):
            max_value = num
            
    val_cor = max_value // ((hyperparemeter/100)+1)

    return (max_value, val_cor)