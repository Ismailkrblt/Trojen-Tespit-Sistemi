import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Veri kümesini yükle
data = pd.read_csv("Trojan_Detection.csv")

# Bellek aşımını önlemek için ilk 10.000 satırı kullan
data = data.iloc[:10000]

# Özellikleri ve etiketleri kodla
lab = LabelEncoder()
for i in data.select_dtypes(include="object").columns.values:
    data[i] = lab.fit_transform(data[i])
data['Class'] = lab.fit_transform(data['Class'])

# Veriyi eğitim ve test kümelerine ayır
x = data.iloc[:, 0:-2]
y = data.iloc[:, -1]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)

# AdaBoostClassifier'ı başlat
model = AdaBoostClassifier(n_estimators=50, learning_rate=1, random_state=42)

# Modeli eğitim verisi üzerinde uygula
model.fit(x_train, y_train)

# Test kümesi sonuçlarını tahmin et
y_pred = model.predict(x_test)

# Doğruluk hesapla
accuracy = accuracy_score(y_test, y_pred)
print(f'Doğruluk: {accuracy:.2f}')

# Karışıklık Matrisi
conf_matrix = confusion_matrix(y_test, y_pred)
print(f'AdaBoostClassifier için Karışıklık Matrisi:\n{conf_matrix}')

# Sınıflandırma Raporu
class_report = classification_report(y_test, y_pred)
print(f'AdaBoostClassifier için Sınıflandırma Raporu:\n{class_report}')
