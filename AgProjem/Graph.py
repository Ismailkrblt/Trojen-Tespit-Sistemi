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

# IP adreslerini düzelt ve sayısal değere dönüştür
def duzelt_ve_donus(ip):
    """Noktalı virgülü (,) ondalık noktaya (.) dönüştürür ve gereksiz boşlukları kaldırır."""
    ip = re.sub(r'[^\d\-+\.]', "", ip).replace(",", ".")  # Noktalı virgülü ve gereksiz karakterleri temizle
    try:
        # IP adresini IPv4Address nesnesine dönüştür
        ip = ipaddress.IPv4Address(ip)
        return int(ip)  # IPv4Address nesnesini tam sayıya dönüştür
    except ipaddress.AddressValueError:
        return None  # Geçersiz IP adresi ise None döndür

# IP adreslerini düzelt ve sayısal değere dönüştür
data[" Source IP"] = data[" Source IP"].apply(duzelt_ve_donus)
data[" Destination IP"] = data[" Destination IP"].apply(duzelt_ve_donus)

# Eksik veya geçersiz IP adreslerini içeren satırları kaldır
data = data.dropna(subset=[" Source IP", " Destination IP"])

# Graf oluştur
G = nx.Graph()

# Her bağlantıyı bir kenar olarak ekle
for i in range(len(data)):
    G.add_edge(data[" Source IP"].iloc[i], data[" Destination IP"].iloc[i])

# Her köşeye "Trojan" veya "Benign" etiketi ekle
for i in range(len(data)):
    source_ip = data[" Source IP"].iloc[i]
    dest_ip = data[" Destination IP"].iloc[i]
    if source_ip not in G.nodes:
        G.add_node(source_ip)
    if dest_ip not in G.nodes:
        G.add_node(dest_ip)
    # Düğümlerin "Class" özelliğini ekle
    if data["Class"].iloc[i] == 1:
        G.nodes[source_ip]["Class"] = "Trojan"
        G.nodes[dest_ip]["Class"] = "Trojan"
    else:
        G.nodes[source_ip]["Class"] = "Benign"
        G.nodes[dest_ip]["Class"] = "Benign"

# Grafı görselleştir
plt.figure(figsize=(15, 10))

# Düğümleri daha düzenli bir şekilde yerleştirmek için kamada_kawai_layout düzenleme algoritmasını kullanalım
pos = nx.kamada_kawai_layout(G)

# Her bir düğüm için uygun renkleri oluştur
renkler = ["red" if G.nodes[node].get("Class") == "Trojan" else "green" for node in G.nodes]

# Grafı düzenle
plt.title("Trojen ve Benign Bağlantılar")
nx.draw_networkx_nodes(G, pos, node_color=renkler, node_size=300, alpha=0.7)
nx.draw_networkx_edges(G, pos, width=2, alpha=0.5)  # Kenarları kalınlaştıralım
nx.draw_networkx_labels(G, pos, font_size=8)  # Düğüm etiketlerini ekle
plt.axis('off')
plt.show()

# Dönüştürülmüş grafı kaydet
nx.write_gexf(G, "dönüştürülmüş_graf.gexf")
