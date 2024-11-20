import argparse
import sys

def generate_report():
    pass

def train_model(filename:str):
    pass

def train_on_directory(directory_path:str):
    pass

def analyze_file(filename:str):
    pass

def analyze_directory(directory_path:str):
    pass

def main(*args):
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