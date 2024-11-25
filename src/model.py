import glob
import os
import json
import numpy.typing as npt
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.base import BaseEstimator
from src.helpers import load_model, save_model, load_data


with open("./settings.json") as f:
    settings = json.load(f)


def train_model(data: npt.ArrayLike, features: npt.ArrayLike) -> BaseEstimator:
    """A function to train a model

    Args:
        data (npt.ArrayLike): The data for the model to be trained on
        features (npt.arraylike): A list of all the features of the model

    Returns:
        BaseEstimator: The model that has been fitted
    """
    MODEL_PATH = f"{os.getcwd()}/models/{settings['MODEL']}"

    model = IsolationForest(n_jobs=-1, random_state=0)

    print("Fitting Model...")
    model.fit(data[features])

    if _old_model_exists():
        save_model(model, is_new_model=False, model_path=MODEL_PATH)
        return

    path = save_model(model)
    settings["MODEL"] = path.split("/")[-1] #the path will be fully formed
    with open("./settings.json", "w") as file:
        file.write(json.dumps(settings))
    return model


def train_on_file(file_path:str) -> None:
    """A function to train a model on a single capture file

    Args:
        file_path (str): The path to the file to be trained on
    """
    print(f"Training on file: {file_path}")
    data, features = load_data(file_path)

    train_model(data, features)


def train_on_directory(directory_path:str) -> None:
    """A function to train a machine learning model on pcaps in a directory

    Args:
        directory_path (str): Path to directory
    """
    print(f"Training on all pcaps in directory: {directory_path}")
    pcaps = glob.glob(os.path.join(f"{os.getcwd()}{directory_path.replace('.','', 1)}", '*.pcap'))

    captures = []
    features = []
    for capture in pcaps:
        df, features = load_data(capture)
        captures.append(df)

    captures = pd.concat(captures)

    train_model(captures, features)


def _old_model_exists() -> bool:
    """A function to check if an old model exists in the settings

    Returns:
        bool: True if a model exists in the settings
    """
    return settings["MODEL"] != ""