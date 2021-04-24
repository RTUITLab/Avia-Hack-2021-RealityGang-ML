import base64
from joblib import dump, load
from .preprocessing import file_to_features
import numpy as np
import base64
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from joblib import dump, load


def process_file(binary_file):
    model = load('main_app/models/xgboost1.joblib')
    features, ids = file_to_features(binary_file)
    labels = model.predict(features)
    answers = {}
    for i in range(len(ids)):
        answers[str(ids[i])] = int(labels[i])
    return answers


def str_to_base64(str_file):
    return base64.b64encode(str_file.encode('utf-8'))


def make_files(base64_str, answers):
    str_file = base64.b64decode(base64_str).decode('utf-8')
    correct = ''
    incorrect = ''
    for line in str_file.split('\n'):
        track_id = line.split(" ")[1][1:-1]
        if answers[track_id] == 0:
            correct += line + '\n'
        else:
            incorrect += line + '\n'

    correct = correct.strip()
    incorrect = incorrect.strip()

    return str_to_base64(correct), str_to_base64(incorrect)
