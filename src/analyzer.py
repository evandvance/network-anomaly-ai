import glob
import os
from src.helpers import load_model, load_data
import pandas as pd
import json


with open("./settings.json") as f:
    settings = json.load(f)


def analyze_file(filename:str) -> pd.DataFrame:
    print(f"File to analyze: {filename}")
    MODEL_PATH = f"{os.getcwd()}/models/{settings['MODEL']}"
    data, features = load_data(filename)
    model = load_model(MODEL_PATH)

    if model == None:
        raise Exception("No Model Found... Please train a new one.")

    data["Predictions"] = model.predict(data[features])

    data["Predictions"] = data["Predictions"].map(lambda val: "Attack" if val == -1 else "Normal")

    return data


def analyze_directory(directory_path:str) -> pd.DataFrame:
    directory = os.getcwd() + directory_path.replace('.','')
    print(f"Analyzing Directory: {directory}")
    pcaps = glob.glob(os.path.join(f"{directory}", '*.pcap'))

    dataframes = []
    for capture in pcaps:
        dataframes.append(analyze_file(capture))

    return pd.concat(dataframes)
