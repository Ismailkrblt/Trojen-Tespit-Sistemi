import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import re # Düzenli ifadeler için re modülünü içe aktarın


def yazdirilamayan_karakterleri_düzenle(text):
 """U+00A0 (kesilmeyen boşluk) dahil olmak üzere yazdırılamayan karakterleri kaldırır."""
 return re.sub(r'[^\x00-\x7F]+', "", text) # ASCII olmayan karakterleri değiştir


# Veri setini yükle
data = pd.read_csv("Trojan_Detection.csv")

# Kaynak ve hedef IP adreslerini listeye dönüştür (yazdirilamayan_karakterleri_düzenle uygula)
kaynak_ipler = data[" Source IP"].apply(yazdirilamayan_karakterleri_düzenle).tolist()
hedef_ipler = data[" Destination IP"].apply(yazdirilamayan_karakterleri_düzenle).tolist()

# Veri setinde hata kontrolü
print(data.dtypes)

# "Class" sütunundaki boşlukları veri setinin ortalamasıyla doldur
data["Class"] = data["Class"].fillna(data["Class"].mean())

# "Sınıf" sütunundaki NaN değerlerini veri setinin ortalamasıyla doldur
data = data.dropna(subset=["Class"])

# IP sütunlarını sayısal değere dönüştürmeyi dene (potansiyel hataları yönet)
try:
    # IP adreslerinin string biçiminde olduğunu varsayarak (gerekirse ayarlayın)
    kaynak_ipler = pd.to_numeric(kaynak_ipler, errors='coerce')
    hedef_ipler = pd.to_numeric(hedef_ipler, errors='coerce')
except Exception as e:
    print(f"Uyarı: IP adresleri sayısal değere dönüştürülemedi. Hata: {e}")
    # Dönüştürme başarısız olursa, string olarak tutun

# Graf oluştur
G = nx.Graph()

# Her bağlantıyı bir kenar olarak ekle
for i in range(len(data)):
    if data["Class"].iloc[i] == 1:
        G.add_edge(f"{kaynak_ipler[i]}", f"{hedef_ipler[i]}")

# Her köşeye "trojen" veya "zararsız" etiketi ekle
for i in range(len(data)):
    if data["Class"].iloc[i] == 1:
        if f"{kaynak_ipler[i]}" not in G.nodes:
            G.add_node(f"{kaynak_ipler[i]}", Sınıf="Trojen")
        if f"{hedef_ipler[i]}" not in G.nodes:
            G.add_node(f"{hedef_ipler[i]}", Sınıf="Trojen")
    else:
        if f"{kaynak_ipler[i]}" not in G.nodes:
            G.add_node(f"{kaynak_ipler[i]}", Sınıf="Benign")
        if f"{hedef_ipler[i]}" not in G.nodes:
            G.add_node(f"{hedef_ipler[i]}", Sınıf="Benign")

# Grafı görselleştir
plt.figure(figsize=(15, 10))
pos = nx.kamada_kawai(G)

# Grafı düzenle
renkler = []
for i in range(len(data)):
    if data["Class"].iloc[i] == 1:
        renkler.append("red")
    else:
        renkler.append("green")

nx.draw(G, pos, with_labels=True, node_size=150, font_size=12, font_color="black", node_color=renkler)
plt.title("Trojen ve Benign Bağlantılar")
plt.show()

# Dönüştürülmüş grafı kaydet
nx.write_gexf(G, "dönüştürülmüş_graf.gexf")