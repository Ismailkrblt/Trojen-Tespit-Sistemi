import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt

# Verileri ölçeklendirme
scaler = StandardScaler()
scaler.fit(X_train)

X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Modeli tanımlama
model = Sequential()

model.add(Dense(128, input_dim=85, activation='relu'))
model.add(Dense(64, input_dim=85, activation='relu'))

model.add(Dense(64, input_dim=85, activation='relu'))
model.add(Dense(64, input_dim=85, activation='relu'))

# Çıktı katmanı (regresyon için)
model.add(Dense(1, activation='linear'))

model.compile(loss='mse', optimizer='adam', metrics=['mae'])
model.summary()

history = model.fit(X_train_scaled, y_train, validation_split=0.2, epochs=20)

# Doğruluğu görselleştirme
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(loss) + 1)
plt.plot(epochs, loss, 'y', label='Eğitim kaybı')
plt.plot(epochs, val_loss, 'r', label='Doğrulama kaybı')
plt.title('Eğitim ve Doğrulama Kaybı')
plt.xlabel('Epoçlar')
plt.ylabel('Kayıp')
plt.legend()
plt.show()