from datetime import date
import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date
def load_and_process(url_or_csv: str):
    df1 = (
        pd.read_csv(url_or_csv)
        .rename(columns={'comms_num':'num_of_comments'})
        .drop(columns=['url', 'created'])
    )
    df2 = (
        df1.sort_values(by=['timestamp','score'], ascending=True)
        .assign(body_is_null=lambda x: x['body'].isnull())
        .reset_index(drop=True)
    )
    return df2

def corr_matrix(df: pd.DataFrame):
    df1 = pd.DataFrame(data=df, columns=['score', 'num_of_comments', 'body_is_null'])
    cor = df1.corr()
    sns.heatmap(cor, annot=True)
    plt.show()

def score_comments(df: pd.DataFrame):
    sns.scatterplot(data=df, x='num_of_comments', y='score', hue='body_is_null')
    plt.show()
    