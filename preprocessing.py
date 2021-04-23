import pandas as pd
import os
import numpy as np

def time_to_seconds(time: str) -> int:
    h, m, s = map(int, time.split(':'))
    return s + m*60 + h*3600

def calc_angle(x1, y1, x2, y2, x3, y3):
    v1 = ((x2-x1), (y2-y1))
    v2 = ((x3-x2), (y3-y2))
    sqrt1, sqrt2 = np.sqrt([v1[0]**2+v1[1]**2, v2[0]**2+v2[1]**2])
    cos = (v1[0]*v2[0] + v1[1]*v2[1]) / (sqrt1*sqrt2)
    return (cos + 1) / 2

def calc_distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)