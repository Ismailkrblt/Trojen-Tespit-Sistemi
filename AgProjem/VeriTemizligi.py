import pandas as pd

df = pd.read_csv("/kaggle/input/trojan-detection-csv/Trojan_Detection.csv", sep = r',', skipinitialspace = True)

df.head()

df = df.dropna()

df.drop(["Unnamed: 0"], axis = 1).values

df = df.replace("Trojan", 1)
df = df.replace("Benign", 0)

df.head()