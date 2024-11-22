from sklearn.base import BaseEstimator
from typing import Callable
from datetime import datetime, timezone
import numpy.typing as npt
import pandas as pd
from pandas.api.types import is_numeric_dtype
from nfstream import NFStreamer
from sklearn.preprocessing import LabelEncoder
import pickle
import os


def trainer_factory(model: BaseEstimator, X: npt.ArrayLike, y: npt.ArrayLike | None, supervised:bool=False) -> Callable:
    """A function to create trainer functions for estimators. This is done so that a training function
       does not need to be written for each model you are trying to train. Lowers verbosity in codebase.

    Args:
        model (BaseEstimator): The model to be trained by the returned function
        X (npt.ArrayLike): The features of the model
        y (npt.ArrayLike | None): The labels for the model
        supervised (bool, optional): If you are creating supervised models this must be set to true. It asserts that the labels exist. Defaults to False.

    Returns:
        Callable: A function to train models by passing in the kwargs.
    """
    def trainer(**kwargs) -> tuple[BaseEstimator, str]:
        if supervised and y == None:
            raise Exception("y Must be defined when using a supervised model")
        mdl = model(**kwargs).fit(X, y) if supervised else model(**kwargs).fit(X)
        return mdl

    return trainer


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
