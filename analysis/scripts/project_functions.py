from datetime import date
import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md
from datetime import date

'''
Milestone 2: Task - 3 is completed here
'''
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
    sns.heatmap(cor, annot=True).set_title('Correlation between fields')
    plt.show()

def score_comments(df: pd.DataFrame):
    sns.scatterplot(data=df, x='num_of_comments', y='score', hue='body_is_null').set_title('Impact of Body on Score and Comments')
    plt.show()

def against_timestamp(df: pd.DataFrame):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    fig, ax = plt.subplots()
    sns.lineplot(ax=ax, x='timestamp', y='score', data=df).set_title('Score at various timestamps')
    # specify the position of the major ticks at the beginning of the week
    ax.xaxis.set_major_locator(md.WeekdayLocator(byweekday = 1))
    # specify the format of the labels as 'year-month-day'
    ax.xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
    # (optional) rotate by 90° the labels in order to improve their spacing
    plt.setp(ax.xaxis.get_majorticklabels(), rotation = 90)
    ax.xaxis.set_minor_locator(md.DayLocator(interval = 1))
    plt.show()
    