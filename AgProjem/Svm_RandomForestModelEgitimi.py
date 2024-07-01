import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import time

data = pd.read_csv("Trojan_Detection.csv", nrows=1000)

X = data.drop(columns=['Class'])
y = data['Class']

numeric_columns = X.select_dtypes(include=['float64', 'int64']).columns
categorical_columns = X.select_dtypes(include=['object']).columns

# Veriyi eğitim ve test setlerine ayırın
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_columns),
        ('cat', categorical_transformer, categorical_columns)
    ])

start_time = time.time()
svm_model = Pipeline(steps=[('preprocessor', preprocessor),
                            ('classifier', SVC(kernel='rbf', C=0.1, gamma='scale'))])
svm_model.fit(X_train, y_train)
svm_training_time = time.time() - start_time

start_time = time.time()
rf_model = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', RandomForestClassifier(n_estimators=50, random_state=42))])
rf_model.fit(X_train, y_train)
rf_training_time = time.time() - start_time

svm_predictions = svm_model.predict(X_test)
rf_predictions = rf_model.predict(X_test)

svm_accuracy = accuracy_score(y_test, svm_predictions)
rf_accuracy = accuracy_score(y_test, rf_predictions)

print("SVM Doğruluk:", svm_accuracy)
print("Random Forest Doğruluk:", rf_accuracy)
print("SVM Eğitim Süresi:", svm_training_time, "saniye")
print("Random Forest Eğitim Süresi:", rf_training_time, "saniye")

# Sınıflandırma raporunu yazdırın
print("SVM Sınıflandırma Raporu:")
print(classification_report(y_test, svm_predictions))

print("Random Forest Sınıflandırma Raporu:")
print(classification_report(y_test, rf_predictions))

results = pd.DataFrame({
    "Model": ["SVM", "Random Forest"],
    "Accuracy": [svm_accuracy, rf_accuracy]
})

plt.figure(figsize=(10, 5))
sns.barplot(x="Model", y="Accuracy", data=results)
plt.title("Model Doğruluk Karşılaştırması")
plt.ylim(0, 1)  # Doğruluk değerleri 0 ile 1 arasında olmalı
plt.show()