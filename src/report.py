import pandas as pd

def generate_report(predictions: pd.DataFrame, filename:str):
    print(f"Saving results to {filename }.csv")
    predictions.to_csv(filename + ".csv")
