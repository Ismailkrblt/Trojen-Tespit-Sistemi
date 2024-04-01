import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Veri setini yükle
data = pd.read_csv("Trojan_Detection.csv")

# Kaynak ve hedef IP adreslerini ve portları listeye dönüştür
kaynak_ipler = data[" Source IP"].tolist()
hedef_ipler = data[" Destination IP"].tolist()
kaynak_portlar = data[" Source Port"].tolist()
hedef_portlar = data[" Destination Port"].tolist()

# Graf oluştur
G = nx.Graph()

# Her bağlantıyı bir kenar olarak ekle
for i in range(len(kaynak_ipler)):
    G.add_edge(f"{kaynak_ipler[i]}:{kaynak_portlar[i]}", f"{hedef_ipler[i]}:{hedef_portlar[i]}")

# Her köşeye "trojen" veya "benign" etiketi ekle
for i in range(len(data)):
    if data["Class"][i] == 1:
        G.nodes[kaynak_ipler[i]+":"+str(kaynak_portlar[i])]["Class"] = "Trojen"
        G.nodes[hedef_ipler[i]+":"+str(hedef_portlar[i])]["Class"] = "Trojen"
    else:
        G.nodes[kaynak_ipler[i]+":"+str(kaynak_portlar[i])]["Class"] = "Benign"
        G.nodes[hedef_ipler[i]+":"+str(hedef_portlar[i])]["Class"] = "Benign"

# Grafı görselleştir
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)  # Grafı düzenle
nx.draw(G, pos, with_labels=True, node_size=100, font_size=8, font_color="black")
plt.title("Trojan ve Benign Bağlantılar")
plt.show()

# Dönüştürülmüş grafı kaydet
nx.write_gpickle(G, "transformed_graph.gpickle")
