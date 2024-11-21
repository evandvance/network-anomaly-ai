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


def train_model(filename:str, model:IsolationForest | None = None)-> int:

    if not model or not settings["MODEL"]:
        model = trainer_factory(IsolationForest, X_train, y_train)()

#This is just a start, it will need to be changed...
def train_on_directory(directory_path:str)-> int:
    pcaps = glob.glob(os.path.join(f"{os.getcwd()}{directory_path.replace(".","")}", '*.pcap'))

    for capture in pcaps:
        train_model(capture)

    return 0