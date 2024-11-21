import glob
import os
from nfstream import NFStreamer
from helpers import load_model
from report import generate_report
import json

settings = json.load("./settings.json")
MODEL_PATH = f"{os.getcwd()}/models/{settings["MODEL"]}"

def analyze_file(filename:str) -> int:
    streamer = NFStreamer(source=filename, statistical_analysis=True, )
    df = streamer.to_pandas(columns_to_anonymize=())

    model = load_model(MODEL_PATH)

    #There is def a bug here. I need to look at what the streamer spits out to know how to do the feature accessing
    predictions = model.predict(df[model.columns])

    generate_report(predictions)

    return 0


def analyze_directory(directory_path:str) -> int:
    pcaps = glob.glob(os.path.join(f"{os.getcwd()}{directory_path.replace(".","")}", '*.pcap'))

    for capture in pcaps:
        analyze_file(capture)

    return 0
