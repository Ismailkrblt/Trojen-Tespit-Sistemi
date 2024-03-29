import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Veri setini yükle
df = pd.read_csv('Trojan_Detection.csv')  

# Veri setinin dosya yolunu düzenleyin
df = pd.DataFrame(df)

# Trojen ve benign dosyaların sayısını source IP'ye göre karşılaştır
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Source IP', hue='Class')
plt.title('Trojen ve Benign Dosyaların Source IP Karşılaştırması')
plt.xlabel('Source IP')
plt.ylabel('Dosya Sayısı')
plt.show()
