import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import re
import ipaddress

# Veri setini yükle
data = pd.read_csv("/kaggle/input/trojan-detection-csv/Trojan_Detection.csv")

# Eksik değerleri kontrol et
print("Eksik Değerler:")
print(data.isnull().sum())

# Veri türlerini kontrol et
print("\nVeri Türleri:")
print(data.dtypes)

# IP adreslerini doğrula ve sayısal değere dönüştür
def validate_and_convert(ip):
    """Noktalı virgülü (,) ondalık noktaya (.) dönüştürür ve gereksiz boşlukları kaldırır."""
    ip = re.sub(r'[^\d\.]', "", ip).replace(",", ".")  # Noktalı virgülü ve gereksiz karakterleri temizle
    try:
        # IP adresini IPv4Address nesnesine dönüştür
        ip = ipaddress.IPv4Address(ip)
        return int(ip)  # IPv4Address nesnesini tam sayıya dönüştür
    except ipaddress.AddressValueError:
        return None  # Geçersiz IP adresi ise None döndür

# IP adreslerini doğrula ve sayısal değere dönüştür
data[" Source IP"] = data[" Source IP"].apply(validate_and_convert)
data[" Destination IP"] = data[" Destination IP"].apply(validate_and_convert)

# Eksik veya geçersiz IP adreslerini içeren satırları kaldır
data = data.dropna(subset=[" Source IP", " Destination IP"])

# Graf oluştur
G = nx.Graph()

# Her bağlantıyı bir kenar olarak ekle
for _, row in data.iterrows():
    G.add_edge((row[" Source IP"], row[" Source Port"]), (row[" Destination IP"], row[" Destination Port"]), Class=row["Class"])

# Grafı görselleştir
plt.figure(figsize=(15, 10))

# Düğümleri daha düzenli bir şekilde yerleştirmek için kamada_kawai_layout düzenleme algoritmasını kullanalım
pos = nx.kamada_kawai_layout(G)

# Her bir düğüm için uygun renkleri oluştur
colors = {"Trojan": "red", "Benign": "green"}
node_colors = [colors[G.nodes[node].get("Class", "Benign")] for node in G.nodes]

# Grafı düzenle
plt.title("Trojen ve Benign Bağlantılar")
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=300, alpha=0.7)
nx.draw_networkx_edges(G, pos, width=2, alpha=0.5)  # Kenarları kalınlaştıralım
nx.draw_networkx_labels(G, pos, font_size=8)  # Düğüm etiketlerini ekle
plt.axis('off')
plt.show()

# Dönüştürülmüş grafı kaydet
nx.write_gexf(G, "dönüştürülmüş_graf.gexf")
