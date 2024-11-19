from sklearn.base import BaseEstimator
from typing import Callable, Dict
import numpy.typing as npt

def trainer_factory(model: BaseEstimator, X: npt.ArrayLike, y: npt.ArrayLike, supervised:bool=False) -> Callable:
    def trainer(**kwargs) -> BaseEstimator:
        return model(**kwargs).fit(X, y) if supervised else model(**kwargs).fit(X)
    return trainer
