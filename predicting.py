import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from joblib import dump, load
from preprocessing import file_to_features


def process_file(binary_file):
    model = load('models/xgboost1.joblib')
    features, ids = file_to_features(binary_file)
    labels = model.predict(features)
    answers = {}
    for i in range(ids.shape[0]):
        answers[str(ids[i])] = int(labels[i])
    return answers


if __name__ == '__main__':
    #Load model
    with open('data/BadTracksHackaton1801.txt', 'rb') as file:
        binary_file = file.read()
    print(process_file(binary_file))
    
    