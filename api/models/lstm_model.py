
#lstm_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

#from base_data.py import get_fake_dataset
from base_data import get_fake_dataset

fake_dataset = get_fake_dataset()

X = fake_dataset.drop('Episodes Occurrences', axis=1).values
y = fake_dataset['Episodes Occurrences'].values

# Standardize the dataset
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Reshape input to be [samples, time steps, features]
X_scaled = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

def get_split_dataset():
    return X_train, X_test, y_train, y_test

# Create the LSTM model
model = Sequential([
    LSTM(50, input_shape=(X_train.shape[1], X_train.shape[2])),
    Dropout(0.2),
    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=10, batch_size=64, validation_data=(X_test, y_test), verbose=2)


# Save the model in HDF5 format
model.save('lstm_model.h5')