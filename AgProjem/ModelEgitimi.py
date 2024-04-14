from scikeras.wrappers import KerasRegressor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt

#Verileri ölçeklendirme
scaler=StandardScaler()
scaler.fit(X_train)

X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Modeli tanımlama
#Daha derin ve daha geniş ağlarla denemeler
model = Sequential()

model.add(Dense(128, input_dim=85, activation='relu'))
model.add(Dense(64, input_dim=85, activation='relu'))

model.add(Dense(64, input_dim=85, activation='relu'))
model.add(Dense(64, input_dim=85, activation='relu'))

#Çıktı
model.add(Dense(1, activation='relu'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

history = model.fit(X_train_scaled, y_train, validation_split=0.2, epochs =20)


#Doğruluğu görselleştirme
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(loss) + 1)
plt.plot(epochs, loss, 'y', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()