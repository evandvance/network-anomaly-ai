import glob
import os
import json
from sklearn.ensemble import IsolationForest
from src.helpers import load_model, save_model, trainer_factory, load_data
from sklearn.metrics import auc, precision_recall_curve, accuracy_score, precision_score, recall_score


with open("./settings.json") as f:
    settings = json.load(f)
MODEL_PATH = f"{os.getcwd()}/models/{settings['MODEL']}"


def train_model(filename:str, train_new:bool=False)-> int:
    train_data = load_data(filename)

#TODO Make this dry
    if not settings["MODEL"] or train_new:
        print("Training new model...")
        model = trainer_factory(IsolationForest, train_data)()
    else:
        model = load_model(MODEL_PATH)

    model.fit(train_data)
    path = save_model(model)
    settings["MODEL"] = path.split("/")[-1] #the path will be fully formed
    json.dumps(settings, "./settings.json")
    return 0


def train_on_directory(directory_path:str)-> int:
    pcaps = glob.glob(os.path.join(f"{os.getcwd()}{directory_path.replace('.','')}", '*.pcap'))

    for capture in pcaps:
        train_model(capture)

    return 0


def eval_model(model, X_test, y_test):
    score = {}
    predictions = model.predict(X_test)

    predictions[predictions == -1] = 0

    precision, recall, _ = precision_recall_curve(y_test, predictions)
    score["auc"] = auc(recall, precision)
    score["precision"] = precision_score(y_test, predictions)
    score["recall"] = recall_score(y_test, predictions)
    score["accuracy"] = accuracy_score(y_test, predictions)

    return score