import pandas as pd
import matplotlib.pyplot as plt

# Verileri yükle
df = pd.read_csv("/kaggle/input/trojan-detection-csv/Trojan_Detection.csv", sep=r',', skipinitialspace=True)

# Hedef kaynak IP'leri
trojan_ip = df[df["Class"] == 1]["Source IP"].to_numpy()
benign_ip = df[df["Class"] == 0]["Source IP"].to_numpy()

# Kutu grafiği
plt.boxplot([trojan_ip, benign_ip], labels=["Trojan", "Benign"], patch_artist=True)
plt.xlabel("Hedef Kaynak IP")
plt.ylabel("Değer")
plt.title("Trojan ve Benign Kaynak IP Dağılımı")
plt.show()

# Histogramlar
plt.figure(figsize=(12, 6)) # Büyük bir figür boyutu ayarlayın
plt.subplot(121)
plt.hist(trojan_ip, color="r", label="Trojan", alpha=0.5)
plt.legend()
plt.title("Trojan Kaynak IP Dağılımı")
plt.subplot(122)
plt.hist(benign_ip, color="g", label="Benign", alpha=0.5)
plt.legend()
plt.title("Benign Kaynak IP Dağılımı")
plt.show()
