import pandas as pd
from sklearn import preprocessing

df = pd.read_csv("Trojan_Detection.csv", sep = r',', skipinitialspace = True)

df = df.dropna()

df.drop(["Unnamed: 0"], axis = 1).values

df = df.replace("Trojan", 1)
df = df.replace("Benign", 0)


number = preprocessing.LabelEncoder()

df["Flow ID"] = number.fit_transform(df["Flow ID"])
df["Source IP"] = number.fit_transform(df["Source IP"])
df["Destination IP"] = number.fit_transform(df["Destination IP"])
df["Timestamp"] = number.fit_transform(df["Timestamp"])

df.head()