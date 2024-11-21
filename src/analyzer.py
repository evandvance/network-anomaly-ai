import glob
import os
from src.helpers import load_model, load_data
from src.report import generate_report
import json


with open("./settings.json") as f:
    settings = json.load(f)
MODEL_PATH = f"{os.getcwd()}/models/{settings['MODEL']}"


def analyze_file(filename:str) -> int:
    data = load_data(filename)
    model = load_model(MODEL_PATH)

    predictions = model.predict(data[model.columns])

    return generate_report(predictions, filename)


def analyze_directory(directory_path:str) -> int:
    pcaps = glob.glob(os.path.join(f"{os.getcwd()}{directory_path.replace('.','')}", '*.pcap'))

    for capture in pcaps:
        analyze_file(capture)

    return 0
