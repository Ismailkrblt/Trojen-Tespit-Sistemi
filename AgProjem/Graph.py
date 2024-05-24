import pandas as pd
import re
import ipaddress
import networkx as nx
import matplotlib.pyplot as plt

def validate_and_convert(ip):
    """Noktalı virgülü (,) ondalık noktaya (.) dönüştürür ve gereksiz boşlukları kaldırır."""
    ip = re.sub(r'[^\d\.]', "", ip).replace(",", ".")  # Noktalı virgülü ve gereksiz karakterleri temizle
    try:
        ip = ipaddress.IPv4Address(ip)
        return int(ip)  # IPv4Address nesnesini tam sayıya dönüştür
    except ipaddress.AddressValueError:
        return None  # Geçersiz IP adresi ise None döndür

# Boş bir DataFrame oluştur
data = pd.DataFrame()

# Veri setini parça parça yükle
chunk_size = 10000
for chunk in pd.read_csv("/kaggle/input/trojan-detection-csv/Trojan_Detection.csv", chunksize=chunk_size):
    chunk[" Source IP"] = chunk[" Source IP"].apply(validate_and_convert)
    chunk[" Destination IP"] = chunk[" Destination IP"].apply(validate_and_convert)
    chunk = chunk.dropna(subset=[" Source IP", " Destination IP"])
    data = pd.concat([data, chunk])

print("Veri Yükleme ve Temizleme Tamamlandı")

# Örnekleme yaparak daha küçük bir veri kümesi oluştur
sample_size = min(len(data), 2000)  # Örnekleme boyutunu küçülttük
sample_data = data.sample(n=sample_size, random_state=1)

# Graf oluştur
G = nx.Graph()

# Her bağlantıyı bir kenar olarak ekle
for _, row in sample_data.iterrows():
    source = (row[" Source IP"], row[" Source Port"])
    destination = (row[" Destination IP"], row[" Destination Port"])
    connection_class = row["Class"]
    G.add_edge(source, destination, Class=connection_class)

# Grafı görselleştir
plt.figure(figsize=(20, 15))  # Graf boyutunu büyüttük

# Düğümleri daha düzenli bir şekilde yerleştirmek için spring_layout düzenleme algoritmasını kullanalım
pos = nx.spring_layout(G)  

# Her bir düğüm için uygun renkleri oluştur
colors = {"Trojan": "red", "Benign": "green"}
node_colors = [colors.get(G.nodes[node].get("Class", "Benign"), "green") for node in G.nodes]

# Her bir kenar için uygun renkleri oluştur
edge_colors = [colors.get(G.edges[edge].get("Class", "Benign"), "green") for edge in G.edges]

# Grafı düzenle
plt.title("Trojan ve Benign Bağlantılar")
nx.draw_networkx_nodes(G, pos, node_size=50, node_color=node_colors, alpha=0.7)
nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=1.5, alpha=0.5)
plt.axis('off')
plt.show()

# Dönüştürülmüş grafı kaydet
nx.write_gexf(G, "dönüştürülmüş_graf.gexf")