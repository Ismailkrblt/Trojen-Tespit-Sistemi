import pandas as pd
import matplotlib.pyplot as plt

veri_seti = pd.read_csv('Trojan_Detection.csv')

# Source IP ve Source Port sütunlarını ayrı ayrı gruplayın
try:
  source_ip_grup = veri_seti.groupby('Source Ip')['Source Port'].count()
  source_port_grup = veri_seti.groupby('Source Port')['Source Ip'].count()
except KeyError as e:
  print(f"Hata: {e}. Lütfen veri setinizi kontrol edin veya kodu ayarlayın.")

# Grafikleri çizin
plt.figure(figsize=(10, 6))

# Source IP sayısı için çubuk grafik
plt.bar(source_ip_grup.index, source_ip_grup.values, color='blue', alpha=0.7, label='Source IP Sayısı')

# Source Port sayısı için çubuk grafik
plt.bar(source_port_grup.index, source_port_grup.values, color='red', alpha=0.7, label='Source Port Sayısı')

plt.xlabel('Source IP veya Source Port')
plt.ylabel('Veri Sayısı')
plt.title('Source IP ve Source Port Karşılaştırması')
plt.legend()
plt.show()
