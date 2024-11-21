import argparse
import sys
from src.analyzer import analyze_directory, analyze_file
from src.model import train_model, train_on_directory


def main(*args) -> int:
    parser = argparse.ArgumentParser(prog="Anomaly Detection in PCAP",
                                     description="A command line program to detect network anomalies in capture files",
                                     epilog="Written by Nima Afsari and Evan Vance")
    parser.add_argument("filename")
    parser.add_argument("-d", "--directory", action="store_true", dest="is_directory")
    parser.add_argument("-t", "--train", action="store_true", dest="is_in_train_mode")
    parser.add_argument("-v", action="version", version="0.0.1")
    parser.add_argument("--DELETE", action="store_true", dest="delete")
    args = parser.parse_args(args)

    if args.delete:
        pass

    if args.is_directory and args.is_in_train_mode:
        return train_on_directory(args.filename)

    if args.is_in_train_mode:
        return train_model(args.filename)

    if args.is_directory:
        return analyze_directory(args.filename)

    return analyze_file(args.filename)

if __name__ == "__main__":
    main(*sys.argv)