import pandas as pd
df= pd.read_excel("titanic3.xls")

print(df.groupby(['pclass','sex'])['survived'].mean())
