import pandas as pd

df = pd.read_csv('resources/mcmd.csv')

def reduce_length(row, max_n=1025):
    res = row['diff'].split(' ')[:max_n]
    return ' '.join(res)
df['diff'] = df.apply(reduce_length, axis=1)

df.to_csv('resources/mcmd_reduced.csv', index=False)