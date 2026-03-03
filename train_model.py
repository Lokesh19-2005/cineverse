import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Flatten, Dense
from tensorflow.keras.optimizers import Adam

# Load cleaned dataset
data = pd.read_csv("movies_cleaned.csv")

# Encode genre
le = LabelEncoder()
data['genre_encoded'] = le.fit_transform(data['genre'])

X = data['genre_encoded']
y = data['imdb']

# Train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build model
model = Sequential()
model.add(Embedding(input_dim=len(le.classes_), output_dim=8))
model.add(Flatten())
model.add(Dense(32, activation='relu'))
model.add(Dense(1))

model.compile(optimizer=Adam(), loss='mse', metrics=['mae'])

# Train model
history = model.fit(X_train, y_train,
                    epochs=10,
                    batch_size=32,
                    validation_data=(X_test, y_test))

# Save model
model.save("recommender_model.h5")

print("Model training complete and saved.")
