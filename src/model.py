import glob
import os
import json
from sklearn.ensemble import IsolationForest
from sklearn.base import BaseEstimator
from src.helpers import load_model, save_model, load_data


with open("./settings.json") as f:
    settings = json.load(f)


def train_model(filename:str, train_new:bool=False) -> BaseEstimator:
    """A function that trains a Machine Learning model on a netflow generate from a pcap.

    Args:
        filename (str): The path to the pcap
        train_new (bool, optional): A boolean that if true trains a new model. Defaults to False.
    
    Returns:
        model (BaseEstimator): the machine learning model that was trained
    """
    print(f"Training Model on file {filename}")

    MODEL_PATH = f"{os.getcwd()}/models/{settings['MODEL']}"
    train_data, features = load_data(filename)

    if not _old_model_exists() or train_new:
        print("Training new model...")
        model = IsolationForest(n_jobs=-1, random_state=0, warm_start=True)
    else:
        model = load_model(MODEL_PATH)

    model.fit(train_data[features])

    if _old_model_exists():
        save_model(model, is_new_model=False, model_path=MODEL_PATH)
        return

    path = save_model(model)
    settings["MODEL"] = path.split("/")[-1] #the path will be fully formed
    with open("./settings.json", "w") as file:
        file.write(json.dumps(settings))
    return model


def train_on_directory(directory_path:str) -> None:
    """A function to train a machine learning model on pcaps in a directoru

    Args:
        directory_path (str): Path to directory
    """
    print(f"Training on all pcaps in directory: {directory_path}")
    pcaps = glob.glob(os.path.join(f"{os.getcwd()}{directory_path.replace('.','', 1)}", '*.pcap'))

    for capture in pcaps:
        train_model(capture)


def _old_model_exists() -> bool:
    """A function to check if an old model exists in the settings

    Returns:
        bool: True if a model exists in the settings
    """
    return settings["MODEL"] != ""