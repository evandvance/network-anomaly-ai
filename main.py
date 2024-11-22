import argparse
import sys
from src.analyzer import analyze_directory, analyze_file
from src.model import train_model, train_on_directory
from src.report import generate_report

parser = argparse.ArgumentParser(prog="Anomaly Detection in PCAP",
                                     description="A command line program to detect network anomalies in capture files",
                                     epilog="Written by Nima Afsari and Evan Vance")
parser.add_argument("filename")
parser.add_argument("-d", "--directory", action="store_true", dest="is_directory")
parser.add_argument("-t", "--train", action="store_true", dest="is_in_train_mode")
parser.add_argument("-v", action="version", version="0.0.1")
parser.add_argument("--DELETE", action="store_true", dest="delete")
args = parser.parse_args()


def main(args) -> None:

    if args.delete:
        pass

    if args.is_directory and args.is_in_train_mode:
        print("Training on Directory...")
        return train_on_directory(args.filename)

    if args.is_in_train_mode:
        print("Training Mode Activated...")
        return train_model(args.filename)

    if args.is_directory:
        print("Analyzing Directory...")
        data = analyze_directory(args.filename)
        return generate_report(data, f"./{args.filename.split('/')[-1]}_Report")

    print("Analyzing file...")
    data = analyze_file(args.filename)
    return generate_report(data, f"./{args.filename.split('/')[-1]}_Report")

if __name__ == "__main__":
    main(args)