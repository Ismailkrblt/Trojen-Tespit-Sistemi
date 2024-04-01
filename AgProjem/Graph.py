import numpy as np
import pandas as pd
import networkx as nx

# Veri setini yükle
data = pd.read_csv("/kaggle/input/trojan-detection-csv/Trojan_Detection.csv")

# Kaynak ve hedef IP adreslerini ve portları listeye dönüştür
kaynak_ipler = data["Source IP"].tolist()
hedef_ipler = data["Destination IP"].tolist()
kaynak_portlar = data["Source Port"].tolist()
hedef_portlar = data["Destination Port"].tolist()

# Graf oluştur
G = nx.Graph()

# Her bağlantıyı bir kenar olarak ekle
for i in range(len(kaynak_ipler)):
    G.add_edge(kaynak_ipler[i]+":"+str(kaynak_portlar[i]), hedef_ipler[i]+":"+str(hedef_portlar[i]))

# Her köşeye "trojen" veya "benign" etiketi ekle
for i in range(len(data)):
    if data["Class"][i] == 1:
        G.nodes[kaynak_ipler[i]+":"+str(kaynak_portlar[i])]["Class"] = "Trojen"
        G.nodes[hedef_ipler[i]+":"+str(hedef_portlar[i])]["Class"] = "Trojen"
    else:
        G.nodes[kaynak_ipler[i]+":"+str(kaynak_portlar[i])]["Class"] = "Benign"
        G.nodes[hedef_ipler[i]+":"+str(hedef_portlar[i])]["Class"] = "Benign"

# Graf transformatörünü oluştur
transformer = nx.GraphTransformer()

# Graf transformatörünü uygula
transformed_graph = transformer.apply(G)

# Dönüştürülmüş grafı kaydet
nx.write_gpickle(transformed_graph, "transformed_graph.gpickle")

# Dönüştürülmüş grafı görselleştirmek için NetworkX'i kullanın
nx.draw(transformed_graph, with_labels=True)
for i in range(len(data)):
    if data["Class"][i] == 1:
        G.nodes[kaynak_ipler[i]+":"+str(kaynak_portlar[i])]["Class"] = "Trojen"
        G.nodes[hedef_ipler[i]+":"+str(hedef_portlar[i])]["Class"] = "Trojen"
    else:
        G.nodes[kaynak_ipler[i]+":"+str(kaynak_portlar[i])]["Class"] = "Benign"
        G.nodes[hedef_ipler[i]+":"+str(hedef_portlar[i])]["Class"] = "Benign"