import numpy as np
import pandas as pd
import os
import datetime
import plotly.express as px

#---------------------------------------VARIABLE DEFINITIONS--------------------------------------------
path_to_dataset = "C:/Users/panos/Desktop/Proyecto Wearables/FrailtyStudy_Datasets/Cuestionarios y Wearables/Wearable Data/raw_data"
# path_to_dataset = f"../../../FrailtyStudy_Datasets/Cuestionarios y Wearables/Wearable Data/raw_data"
phase_names = ['start', 'standup', 'walkingToStore', 'inEntrance', 'walkingToCorrectSection',
                'pickUpItem', 'walkingToCheckout', 'inTheCheckout', 'inItsTurn', 'goToTheExit',
                'inTheExit', 'comingBack', 'inTheStartPoint', 'end']
experiment_id_dict = {
        "CM": np.array([1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 16, 18, 19, 20]),
        "E": np.array([3, 4, 5, 6]),
        "Z": np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 40, 42, 43, 45, 46, 47, 50, 51, 52, 53, 54, 55, 56, 59, 60, 61, 62, 63, 64, 66, 67, 68, 70, 71, 72, 74, 75, 76, 77, 78, 80])
    }

# Sensor types
E4_EDA = 0
E4_HEARTRATE = 1
E4_ACCELEROMETER = 2
E4_GYROSCOPE = 3
E4_TEMPERATURE = 4

SW_HEARTRATE = 10
SW_ACCELEROMETER = 11
SW_GYROSCOPE = 12


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
    os.chdir(path_to_dataset)
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

def read_samsung_data(filepath, columns):
    df = pd.read_csv(filepath, names = columns)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('datetime', inplace=True)

    return df

def get_phase_diff(filepath, columns):

    df = read_samsung_data(filepath, columns)

    df.drop(['day_month_year', 'hour_min_sec_ms'], axis=1, inplace=True)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.drop(['timestamp'], axis=1, inplace=True)
    df.set_index('datetime', inplace=True)
    df['phase_diff'] = df['phase'].diff()
    phase_diff = df[df['phase_diff'] != 0]
    phase_diff.drop(['phase_diff'], axis=1, inplace=True)

    return phase_diff

def plot_figure(df, x, y, phase_diff, phase_names):
    fig = px.line(df, x=x, y=y)

    for i in range(len(phase_diff.index)):
        fig.add_vline(phase_diff.index[i], line_width=1, line_dash="dash", line_color="red")
        text_y = 0.75
        fig.add_annotation(x = phase_diff.index[i], y=text_y, yref="paper", text=phase_names[i], textangle=-90)
    return fig

def get_figure(participant, sensor_type):

    # Get Empatica data
    e4_filepath = f"{path_to_dataset}/{participant}/empatica/"
    if sensor_type == E4_EDA:
        e4_filepath += "EDA.csv"
        y = ['eda']
    
    elif sensor_type == E4_HEARTRATE:
        e4_filepath += "HR.csv"
        y = ['hr']
    
    else:
        print("Sensor type not supported") 
    df = e4_data_to_df(e4_filepath, y)

    # Get phase differences
    file = "es.ugr.frailty.heartrate.csv"
    tw_filepath = f"{path_to_dataset}/{participant}/{file}"
    columns = ['timestamp', 'day_month_year', 'hour_min_sec_ms', 'hr', 'phase']
    
    phase_diff = get_phase_diff(tw_filepath, columns)

    # Get figure
    fig = plot_figure(df, df.index, y, phase_diff, phase_names)

    return fig