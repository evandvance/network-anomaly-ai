from sklearn.base import BaseEstimator
from datetime import datetime, timezone
import pandas as pd
from pandas.api.types import is_numeric_dtype
from nfstream import NFStreamer
from sklearn.preprocessing import LabelEncoder
import pickle
import os


def save_model(model:BaseEstimator, scores: str | None = None, is_new_model:bool=True, model_path: str | None = None) -> str:
    """A function to save a model to your drive.

    Args:
        model (BaseEstimator): The model to be saved
        scores (str | None, optional): Pass the relevant scoring metrics to the function to help identify the model later. Defaults to None.
        is_new_model (bool, optional): This is to help identify when a model has been loaded changed and would like to be saved again with the same name. Defaults to True.
        model_path (str | None, optional): This is the path to save models to. If none a path is generated. Defaults to None.

    Raises:
        Exception: If there is no model path and it is not a new model, it throws an error.

    Returns:
        str: Path to the model
    """
    print("Saving model...")

    if not is_new_model and not model_path:
        raise Exception("Saving an old model requires a path to store it.")

    time = str(datetime.now(timezone.utc)).replace(" ","#")
    path = f"{os.getcwd()}/models/{model.__class__.__name__}_{scores + '_' if scores else ''}{time}.mdl" if is_new_model else model_path

    with open(path,'wb') as f:
        pickle.dump(model,f)
    return path


def load_model(path:str) -> BaseEstimator:
    """A function to load models into memory from a file.

    Args:
        path (str): The path to the model's file

    Returns:
        BaseEstimator: The model loaded from storage
    """
    print(f"Loading model: {path}")
    with open(path, 'rb') as f:
        return pickle.load(f)


def load_data(path:str) -> pd.DataFrame:
    """A function to load data from a pcap into a dataframe.

    Args:
        path (str): Path to the pcap to load

    Returns:
        pd.DataFrame: A dataframe representation of the netflow of the pcap
    """
    print("Loading Data...")

    streamer = NFStreamer(source=path, statistical_analysis=True)

    data = streamer.to_pandas()
    features = data.drop(columns=["id", "expiration_id","src_ip", "src_mac", "src_oui", "dst_ip", "dst_mac","dst_oui"]).columns

    for column in features:
        if not is_numeric_dtype(data[column]):
            data[column] = LabelEncoder().fit_transform(data[column])

    return data, features



