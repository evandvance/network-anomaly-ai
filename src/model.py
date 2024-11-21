import glob
import os
import json
from sklearn.ensemble import IsolationForest
from src.helpers import load_model, save_model, trainer_factory
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import auc, precision_recall_curve, accuracy_score, precision_score, recall_score


settings = json.load("./settings.json")
MODEL_PATH = f"{os.getcwd()}/models/{settings["MODEL"]}"


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


def train_model(filename:str, train_new:bool=False)-> int:
    #TODO Get Data sorted...

    if not settings["MODEL"] or train_new:
        print("Training new model...")
        #this method saves the model once trained automatically
        model, path = trainer_factory(IsolationForest, X_train, y_train)()
        settings["MODEL"] = path.split("/")[-1] #the path will be fully formed
        return 0

    model = load_model(MODEL_PATH)
    model.fit(X_train)
    path = save_model(model)
    settings["MODEL"] = path.split("/")[-1] #the path will be fully formed
    return 0


#This is just a start, it will need to be changed...
def train_on_directory(directory_path:str)-> int:
    pcaps = glob.glob(os.path.join(f"{os.getcwd()}{directory_path.replace(".","")}", '*.pcap'))

    for capture in pcaps:
        train_model(capture)

    return 0