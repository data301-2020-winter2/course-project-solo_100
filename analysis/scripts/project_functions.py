import pandas as pd 
import numpy as np 

def load_and_process(url_or_csv: str):
    df1 = (
        pd.read_csv(url_or_csv)
        .rename(columns={'comms_num':'num_of_comments'})
        .drop(columns=['url', 'created'])
    )
    df2 = (
        df1.sort_values(by=['timestamp','score'], ascending=True)
        .to_csv('../data/processed/processed.csv')
    )
    return df2