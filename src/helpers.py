from sklearn.base import BaseEstimator
from typing import Callable
from datetime import datetime, timezone
import numpy.typing as npt
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