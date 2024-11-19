from sklearn.base import BaseEstimator
from typing import Callable
from datetime import datetime, timezone
import numpy.typing as npt
import pickle
import os

def trainer_factory(model: BaseEstimator, X: npt.ArrayLike, y: npt.ArrayLike, supervised:bool=False) -> Callable:
    def trainer(**kwargs) -> tuple[BaseEstimator, str]:
        mdl = model(**kwargs).fit(X, y) if supervised else model(**kwargs).fit(X)
        path = save_model(mdl)
        return mdl, path

    return trainer

def save_model(model:BaseEstimator) -> str:
    time = str(datetime.now(timezone.utc)).replace(" ","")
    path = f"{os.getcwd()}/models/{model.__class__.__name__}_{time}.mdl"

    with open(path,'wb') as f:
        pickle.dump(model,f)
    return path

def load_model(path:str) -> BaseEstimator:
    with open(path, 'rb') as f:
        return pickle.load(f)