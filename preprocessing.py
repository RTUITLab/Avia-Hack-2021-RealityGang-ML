import pandas as pd
from os.path import join, isfile
from os import listdir
import numpy as np
import math
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
import time

def time_to_seconds(time: str) -> int:
    h, m, s = map(int, time.split(':'))
    return s + m*60 + h*3600

def calc_angle(x1, y1, x2, y2, x3, y3):
    v1 = ((x2-x1), (y2-y1))
    v2 = ((x3-x2), (y3-y2))
    sqrt1, sqrt2 = np.sqrt([v1[0]**2+v1[1]**2, v2[0]**2+v2[1]**2])
    cos = (v1[0]*v2[0] + v1[1]*v2[1]) / ((sqrt1 + 0.01) * (sqrt2 + 0.01))
    return (cos + 1) / 2

def calc_distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def kernel(tupl):
    _, track_data = tupl
    p_index = 0
    min_angle = 2
    max_z_speed = 0
    avg_z_speed = 0
    max_xy_speed = 0
    avg_xy_speed = 0
    max_time_diff = 0
    avg_time_diff = (track_data.iloc[track_data.shape[0] - 1]['time'] - track_data.iloc[0]['time']) / track_data.shape[0]
    for i in range(1, track_data.shape[0]):
        time_diff = track_data.iloc[i]['time'] - track_data.iloc[i - 1]['time']
        if(time_diff == 0):
            time_diff = .001
        if time_diff > max_time_diff:
            max_time_diff = time_diff
        
        if i != track_data.shape[0] - 1:
            angle = calc_angle(track_data.iloc[i - 1]['latitude'], track_data.iloc[i - 1]['longitude'], track_data.iloc[i]['latitude'],
                               track_data.iloc[i]['longitude'], track_data.iloc[i + 1]['latitude'], track_data.iloc[i + 1]['longitude'])
            if angle < min_angle:
                min_angle = angle
                p_index = i
        
        xy_speed = calc_distance(track_data.iloc[i - 1]['latitude'], track_data.iloc[i - 1]['longitude'], 
                                 track_data.iloc[i]['latitude'], track_data.iloc[i]['longitude']) / time_diff
        if xy_speed > max_xy_speed:
            max_xy_speed = xy_speed
        avg_xy_speed += xy_speed
        
        z_speed = abs(track_data.iloc[i-1]['elevation'] - track_data.iloc[i]['elevation']) / time_diff
        if z_speed > max_z_speed:
            max_z_speed = z_speed
        avg_z_speed += z_speed
        
    avg_xy_speed /= track_data.shape[0]
    avg_z_speed /= track_data.shape[0]
    return [min_angle, max_xy_speed, avg_xy_speed, max_z_speed, avg_z_speed, max_time_diff, avg_time_diff]

def get_features(grouped_df):
    pool = Pool(16)
    DATA = pool.map(kernel, grouped_df)
    pool.close()
    pool.join()
    return DATA

if __name__ == '__main__':
    for file in listdir('data'):
        if isfile(join('data', file)):
            path = join('data', file)
            data = pd.read_csv(path, sep=' ', header=None, names=['time', 'id', 'latitude', 'longitude', 'elevation', 'code', 'name'])
            data['time'] = data['time'].apply(time_to_seconds)
            grouped = data.groupby('id')
            grouped_df = [i for i in grouped]
            t = time.time()
            tmp = get_features(grouped_df)
            print(time.time() - t)
            arr = np.array(tmp)
            with open(join('processed', file), 'wb') as f:
                np.save(f, arr)
    #print(grouped_df)
    