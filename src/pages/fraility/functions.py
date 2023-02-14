import numpy as np
import pandas as pd
import os
import datetime



#---------------------------------------VARIABLE DEFINITIONS--------------------------------------------
filepath = f"../../FrailtyStudy_Datasets/Cuestionarios y Wearables/Wearable Data/raw_data"
phase_names = ['start', 'standup', 'walkingToStore', 'inEntrance', 'walkingToCorrectSection',
                'pickUpItem', 'walkingToCheckout', 'inTheCheckout', 'inItsTurn', 'goToTheExit',
                'inTheExit', 'comingBack', 'inTheStartPoint', 'end']
experiment_id_dict = {
        "CM": np.array([1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 16, 18, 19, 20]),
        "E": np.array([3, 4, 5, 6]),
        "Z": np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 40, 42, 43, 45, 46, 47, 50, 51, 52, 53, 54, 55, 56, 59, 60, 61, 62, 63, 64, 66, 67, 68, 70, 71, 72, 74, 75, 76, 77, 78, 80])
    }


#---------------------------------------------METHODS----------------------------------------------------
def split_participant_names(folder_names):
    # GET CM1, CM2, E3, Z7...
    split_folders = pd.DataFrame(columns= ['type', 'id'])
    for folder in folder_names:
        head = folder.rstrip('0123456789')
        tail = folder[len(head):]
        split_folders.loc[(len(split_folders.index))] = [head, tail]

    return split_folders

def get_experiment_names():
    # Access folders through os
    owd = os.getcwd()
    os.chdir(filepath)
    folder_names = [name for name in os.listdir(".") if os.path.isdir(name)]
    os.chdir(owd)

    # Split them and add to df
    return split_participant_names(folder_names)

def e4_data_to_df(filepath, column_names):

    df = pd.read_csv(filepath, names=column_names)

    # Get timestamp and sampling freq
    initial_timestamp = df.iloc[0, 0]
    frecuency = 1/df.iloc[1, 0]
    df.drop([0, 1], inplace=True)

    # Get datetime and add to df
    initial_datetime = datetime.datetime.utcfromtimestamp(initial_timestamp) # + pd.Timedelta(hours=2) # +2 hour to account for different time zone from UTC
    print(initial_timestamp, initial_datetime, frecuency)
    df['datetime'] = pd.date_range(initial_datetime, initial_datetime + pd.Timedelta(seconds=frecuency*df.shape[0]), periods=df.shape[0])
    df.set_index('datetime', inplace=True)

    return df
