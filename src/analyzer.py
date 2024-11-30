import glob
import os
from src.helpers import load_model, load_data
import pandas as pd
import json


with open("./settings.json") as f:
    settings = json.load(f)


def analyze_file(filename:str) -> pd.DataFrame:
    """A function to load a given pcap file into a dataframe and analyze its contents for anomalies

    Args:
        filename (str): The path to the pcap for analyzing

    Raises:
        Exception: If no model is found, it throws an error

    Returns:
        pd.DataFrame: 
            A dataframe representation of the netflow of a pcap file with flows marked
            as Malicoious if they are considered attacks by the model and BENIGN if 
            they are considered normal traffic by the model
    """
    print(f"File to analyze: {filename}")
    MODEL_PATH = f"{os.getcwd()}/models/{settings['MODEL']}"
    data, features = load_data(filename)
    model = load_model(MODEL_PATH)

    if model == None:
        raise Exception("No Model Found... Please train a new one.")

    print("Analyzing...")
    data["Predictions"] = model.predict(data[features])

    data["Predictions"] = data["Predictions"].map(lambda val: "MALICIOUS" if val == -1 else "BENIGN")

    return data


def analyze_directory(directory_path:str) -> pd.DataFrame:
    """This function iterates over all pcaps in a directory running analyze_file on each of them
       and combining their results. See analyze_file for more information.

    Args:
        directory_path (str): The path to the directory to analyze

    Returns:
        pd.DataFrame:
            A dataframe representation of the netflow of a pcap file with flows marked
            as Malicoious if they are considered attacks by the model and BENIGN if 
            they are considered normal traffic by the model
    """
    directory = os.getcwd() + directory_path.replace('.','')
    print(f"Analyzing Directory: {directory}")
    pcaps = glob.glob(os.path.join(f"{directory}", '*.pcap'))

    dataframes = []
    for capture in pcaps:
        dataframes.append(analyze_file(capture))

    return pd.concat(dataframes)
