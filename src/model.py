import glob
import os
import json
from pandas.api.types import is_numeric_dtype
from nfstream import NFStreamer
from sklearn.ensemble import IsolationForest
from src.helpers import load_model, save_model, trainer_factory
from sklearn.preprocessing import LabelEncoder

with open("./settings.json") as f:
    settings = json.load(f)
MODEL_PATH = f"{os.getcwd()}/models/{settings['MODEL']}"


def train_model(filename:str, train_new:bool=False)-> int:
    #TODO Get Data sorted...
    offline_streamer = NFStreamer(source=filename,
                              statistical_analysis=True,
                              splt_analysis=10)

    train_data = offline_streamer.to_pandas(columns_to_anonymize=())

    for column in train_data.columns:
        if is_numeric_dtype(train_data[column]):
            train_data[column] = LabelEncoder().fit_transform(train_data[column])

#TODO Make this dry
    if not settings["MODEL"] or train_new:
        print("Training new model...")
        #this method saves the model once trained automatically
        model, path = trainer_factory(IsolationForest, train_data)()
        settings["MODEL"] = path.split("/")[-1] #the path will be fully formed
        json.dumps(settings, "./settings.json")
        return 0

    model = load_model(MODEL_PATH)
    model.fit(train_data)
    path = save_model(model)
    settings["MODEL"] = path.split("/")[-1] #the path will be fully formed
    json.dumps(settings, "./settings.json")
    return 0


#This is just a start, it will need to be changed...
def train_on_directory(directory_path:str)-> int:
    pcaps = glob.glob(os.path.join(f"{os.getcwd()}{directory_path.replace('.','')}", '*.pcap'))

    for capture in pcaps:
        train_model(capture)

    return 0