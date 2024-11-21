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
    def trainer(**kwargs) -> tuple[BaseEstimator, str]:
        if supervised and y == None:
            raise Exception("y Must be defined when using a supervised model")
        mdl = model(**kwargs).fit(X, y) if supervised else model(**kwargs).fit(X)
        return mdl

    return trainer

def save_model(model:BaseEstimator, scores: str | None = None) -> str:
    time = str(datetime.now(timezone.utc)).replace(" ","")
    path = f"{os.getcwd()}/models/{model.__class__.__name__}_{scores + "_" if scores else None}{time}.mdl"

    with open(path,'wb') as f:
        pickle.dump(model,f)
    return path

def load_model(path:str) -> BaseEstimator:
    with open(path, 'rb') as f:
        return pickle.load(f)

def load_data(path:str) -> pd.DataFrame:
    streamer = NFStreamer(source=path,
                              statistical_analysis=True)

    data = streamer.to_pandas().drop(columns=["src_ip", "src_mac", "src_oui", "dst_ip", "dst_mac","dst_oui"])

    for column in data.columns:
        if not is_numeric_dtype(data[column]):
            data[column] = LabelEncoder().fit_transform(data[column])

    return data
