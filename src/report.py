import pandas as pd

def generate_report(predictions: pd.DataFrame, filename:str):
    predictions.to_csv(filename + ".csv")
