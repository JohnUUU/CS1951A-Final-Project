import pandas as pd
from sqlalchemy import create_engine
import seaborn as sns
import matplotlib.pyplot as plt

# DATA
# https://data.cccnewyork.org/data/table/66/median-incomes#66/107/62/a/a

# read data and get rid of non zip code entries
data = pd.read_csv('demographics/incomes.csv')[3900:]
data["Location"] = data["Location"].apply(lambda x: x.replace("Zip Code ", ""))

# only want 2019 and up
data = data[data["TimeFrame"] >= 2019] 

# Only want these 2 columns
data = data[["Location", "Data"]]

# Change types
data["Location"] = data["Location"].astype(str)
data["Data"] = data["Data"].astype(int)

# Filter out outliers
#data = data[data["Data"] <= 180000] 

# change column names
data.columns = ["ZIP", "MED_INCOME"]
print(data.head())
print(data.shape)
print(data.describe())

#ax = sns.boxplot(data["MED_INCOME"])
#plt.show()

# Save to SQL database
disk_engine = create_engine('sqlite:///database/final.db')
data.to_sql('incomes', disk_engine, if_exists='replace', index=False)
