import argparse
import sys
import os
import glob
from nfstream import NFStreamer
from helpers import load_model

MODEL = "IsolationForest_2024-11-1918:00:35.183625+00:00.mdl"
MODEL_PATH = f"{os.getcwd()}/models/{MODEL}"

def generate_report():
    pass

def train_model(filename:str)-> int:
    pass

def train_on_directory(directory_path:str)-> int:
    pass

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


def main(*args) -> int:
    parser = argparse.ArgumentParser(prog="Anomaly Detection in PCAP",
                                     description="A command line program to detect network anomalies in capture files",
                                     epilog="Written by Nima Afsari and Evan Vance")
    parser.add_argument("filename")
    parser.add_argument("-d", "--directory", action="store_true", dest="is_directory")
    parser.add_argument("-t", "--train", action="store_true", dest="is_in_train_mode")
    parser.add_argument("-v", action="version", version="0.0.1")
    args = parser.parse_args(args)

    if args.is_directory and args.is_in_train_mode:
        return train_on_directory(args.filename)

    if args.is_in_train_mode:
        return train_model(args.filename)

    if args.is_directory:
        return analyze_directory(args.filename)

    return 0

if __name__ == "__main__":
    main(*sys.argv)