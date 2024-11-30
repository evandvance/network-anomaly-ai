import argparse
from src.analyzer import analyze_directory, analyze_file
from src.model import train_on_file, train_on_directory
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
    """The entry point of the program. This is a CLI tool to use a machine learning model to
       try to identify malicous traffic in a network. The flags are as follows:

       filename: the file or directory the program is meant to analyze
       -d or --directory: This flag is used to tell the program to treat the filename as a directory
       -t or --train: This flag is used to signal to the program that it is to use the filename to train the model.
       -v: Shows the program version
       --DELETE: ***DANGEROUS*** Deletes the model and clears the settings. 

    Args:
        args (list[str]): The arguments from a command line. These include flags and directories

    """
    if args.delete:
        pass

    if args.is_directory and args.is_in_train_mode:
        print("Training on Directory...")
        return train_on_directory(args.filename)

    if args.is_in_train_mode:
        print("Training Mode Activated...")
        return train_on_file(args.filename)

    if args.is_directory:
        print("Analyzing Directory...")
        data = analyze_directory(args.filename)
        return generate_report(data, f"./reports/{args.filename.split('/')[-1]}")

    print("Analyzing file...")
    data = analyze_file(args.filename)
    return generate_report(data, f"./reports/{args.filename.split('/')[-1]}")

if __name__ == "__main__":
    main(args)