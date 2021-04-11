import pandas as pd 
import numpy as np
from pandas.core.frame import DataFrame 
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md
import re

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

def pairplot(df: pd.DataFrame):
    df.drop(columns=['timestamp'])
    pairplot = sns.pairplot(df)
    pairplot.fig.suptitle('All fields against each other', y=1.1)
    plt.show()

def boxplot(df: pd.DataFrame):
    df.boxplot(column=['score', 'num_of_comments']).set_title('Score and Comments Distribution')
    plt.show()

def contains_gme(df: pd.DataFrame):
    count = 0
    t = df['title']
    b = df['body']
    for i in range(t.size):
       if((t[i] != None and t[i] != np.NaN and re.search(r"gme", str(t[i]), flags=re.IGNORECASE | re.MULTILINE) != None) or (b[i] != None and b[i] != np.NaN and re.search(r"gme", str(b[i]), flags=re.IGNORECASE | re.MULTILINE) != None)):
           count = count + 1
    
    pieDf = pd.DataFrame({'posts': [count, t.size - count]}, index=['$GME', '$OTHERS'])
    pieDf.plot(kind='pie', y='posts')
    plt.legend(loc='upper left')
    plt.show()
    
def prep_tableau(df: pd.DataFrame, path: str):
    df.drop(columns=['id'], inplace=True)
    t = df['title']
    b = df['body']
    contains_gme = []
    for i in range(t.size):
        if((t[i] != None and t[i] != np.NaN and re.search(r"gme", str(t[i]), flags=re.IGNORECASE | re.MULTILINE) != None) or (b[i] != None and b[i] != np.NaN and re.search(r"gme", str(b[i]), flags=re.IGNORECASE | re.MULTILINE) != None)):
            contains_gme.append(True)
        else:
            contains_gme.append(False)

    df['contains_gme'] = contains_gme

    df.dropna(subset=['title', 'score', 'num_of_comments', 'body_is_null', 'timestamp', 'contains_gme'], inplace=True)
    df.drop(columns=['body', 'title'], inplace=True)
    df['score'] = df['score'].astype(int)
    df['num_of_comments'] = df['num_of_comments'].astype(int)
    
    df.to_csv(path)
    return df
    
