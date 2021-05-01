import pandas as pd
from os.path import join, isfile
from os import listdir
import numpy as np
import math
from multiprocessing import Pool
import time
from io import BytesIO
import base64


def time_to_seconds(time: str) -> int:
    h, m, s = map(int, time.split(':'))
    return s + m*60 + h*3600


def calc_angle(v1, v2):
    cos = (v1[0] * v2[0] + v1[1] * v2[1]) / ((v1[0]**2 + v1[1]**2 + 0.01) * (v2[0]**2 + v2[1]**2 + 0.01))
    return (cos + 1) / 2


def calc_distance(v):
    return math.sqrt(v[0]**2 + v[1]**2)


def kernel(tupl):
    _, track_data = tupl
    min_angle = 2
    max_z_speed = 0
    avg_z_speed = 0
    max_xy_speed = 0
    avg_xy_speed = 0
    max_time_diff = 0
    avg_time_diff = (track_data.iloc[track_data.shape[0] - 1]['time'] - track_data.iloc[0]['time']) / track_data.shape[0]
    v_prev = (track_data.iloc[1]['latitude'] - track_data.iloc[0]['latitude'], track_data.iloc[1]['longitude'] - track_data.iloc[0]['longitude'])
    v = ()
    for i in range(1, track_data.shape[0]):
        time_diff = track_data.iloc[i]['time'] - track_data.iloc[i - 1]['time']
        if time_diff == 0:
            time_diff = .001
        if time_diff > max_time_diff:
            max_time_diff = time_diff
        
        if i != track_data.shape[0] - 1:
            v = (track_data.iloc[i + 1]['latitude'] - track_data.iloc[i]['latitude'], track_data.iloc[i + 1]['longitude'] - track_data.iloc[i]['longitude'])
            angle = calc_angle(v_prev, v)
            if angle < min_angle:
                min_angle = angle
        
        xy_speed = calc_distance(v_prev) / time_diff
        if xy_speed > max_xy_speed:
            max_xy_speed = xy_speed
        avg_xy_speed += xy_speed
        
        z_speed = abs(track_data.iloc[i-1]['elevation'] - track_data.iloc[i]['elevation']) / time_diff
        if z_speed > max_z_speed:
            max_z_speed = z_speed
        avg_z_speed += z_speed
        if i != track_data.shape[0] - 1:
            v_prev = v
        
    avg_xy_speed /= track_data.shape[0]
    avg_z_speed /= track_data.shape[0]
    return [min_angle, max_xy_speed, avg_xy_speed, max_z_speed, avg_z_speed, max_time_diff, avg_time_diff]


def get_features(grouped_df):
    pool = Pool(16)
    DATA = pool.map(kernel, grouped_df)
    pool.close()
    pool.join()
    return DATA


def file_to_features(binary_file):
    data = pd.read_csv(BytesIO(base64.b64decode(binary_file)), sep=' ', header=None, names=['time', 'id', 'latitude', 'longitude', 'elevation', 'code', 'name'])
    data['time'] = data['time'].apply(time_to_seconds)
    grouped = data.groupby('id')
    grouped_df = [i for i in grouped]
    tmp = get_features(grouped_df)
    features = np.array(tmp)
    return (features, list(grouped.groups.keys()))


def testing(filename):
    data = pd.read_csv(filename, sep=' ', header=None, names=['time', 'id', 'latitude', 'longitude', 'elevation', 'code', 'name'])
    data['time'] = data['time'].apply(time_to_seconds)
    grouped = data.groupby('id')
    grouped_df = [i for i in grouped]
    tmp = get_features(grouped_df)
    features = np.array(tmp)
    return features, list(grouped.groups.keys())


if __name__ == "__main__":
    for i in range(4):
        t = time.time()
        testing('data/BadTracksHackaton1801.txt')
        print(time.time() - t)