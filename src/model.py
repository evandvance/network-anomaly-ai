import glob
import os
import json
from sklearn.ensemble import IsolationForest
from src.helpers import load_model, save_model, load_data


with open("./settings.json") as f:
    settings = json.load(f)


def train_model(filename:str, train_new:bool=False)-> int:
    print(f"Training Model on file {filename}")

    MODEL_PATH = f"{os.getcwd()}/models/{settings['MODEL']}"
    train_data, features = load_data(filename)

    if settings["MODEL"] == "" or train_new:
        print("Training new model...")
        model = IsolationForest()
    else:
        model = load_model(MODEL_PATH)

    model.fit(train_data[features])

    if settings["MODEL"] != "":
        path = save_model(model, is_new_model=False, model_path=MODEL_PATH)
        return 0


    path = save_model(model)
    settings["MODEL"] = path.split("/")[-1] #the path will be fully formed
    with open("./settings.json", "w") as file:
        file.write(json.dumps(settings))
    return 0


def train_on_directory(directory_path:str)-> int:
    pcaps = glob.glob(os.path.join(f"{os.getcwd()}{directory_path.replace('.','', 1)}", '*.pcap'))

    for capture in pcaps:
        train_model(capture)

    return 0
