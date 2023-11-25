import os
import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.utils import to_categorical
from keras.preprocessing.sequence import pad_sequences
import librosa
from sklearn.model_selection import train_test_split

# Fonction pour extraire les MFCC à partir d'un fichier audio
def extract_mfcc(file_path, num_mfcc=13, n_fft=2048, hop_length=512):
    signal, sr = librosa.load(file_path)
    mfccs = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=num_mfcc, n_fft=n_fft, hop_length=hop_length)
    return mfccs.T
max_sequence_length = 49  # Remplacez par la longueur maximale souhaitée

# Fonction pour charger les données depuis des dossiers et sous-dossiers
def load_data_from_folders(root_folder, max_sequence_length=None):
    data = []
    labels = []
    label_to_index = {}

    for i, label in enumerate(os.listdir(root_folder)):
        label_path = os.path.join(root_folder, label)
        if os.path.isdir(label_path):
            label_to_index[label] = i

            for sublabel in os.listdir(label_path):
                sublabel_path = os.path.join(label_path, sublabel)
                if os.path.isdir(sublabel_path):
                    for file_name in os.listdir(sublabel_path):
                        file_path = os.path.join(sublabel_path, file_name)
                        try:
                            mfccs = extract_mfcc(file_path)
                            # Limiter la longueur de la séquence si nécessaire
                            if max_sequence_length:
                              mfccs = mfccs[:max_sequence_length, :]

                            data.append(mfccs)
                            labels.append(i)
                        except Exception as e:
                            print(f"Erreur lors du traitement de {file_path}: {e}")

    return data, labels, label_to_index

# Charger les données
root_folder = "/Users/abdelwahed/Desktop/dataset-collection-LOW/dataset-collection-LOW/"

data, labels, label_to_index = load_data_from_folders(root_folder, max_sequence_length)
print(len(label_to_index))
#print(data)
print(len(labels))

# Utilisez pad_sequences pour garantir que toutes les séquences ont la même longueur
X_padded = pad_sequences(data, dtype='float32', padding='post')

num_classes = len(label_to_index)


# Créer un modèle CNN simple
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(X_padded.shape[1], X_padded.shape[2], 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

# Convertissez les étiquettes en catégories
y = to_categorical(np.array(label_to_index))
print(len(y))

X_train, X_test, y_train, y_test = train_test_split(X_padded, y, test_size=0.2, random_state=42)

# Compiler le modèle
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entraîner le modèle
model.fit(X_train.reshape(*X_train.shape, 1), y_train, epochs=10, batch_size=32, validation_split=0.2)
#model.fit(X_padded.reshape(*X_padded.shape, 1), y, epochs=10, batch_size=32, validation_split=0.2)

# Évaluer le modèle sur un ensemble de test si disponible
loss, accuracy = model.evaluate(X_test.reshape(*X_test.shape, 1), y_test)
print(f"Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}")

#prédictions
new_audio_path = "/Users/abdelwahed/Desktop/dataset-collection-LOW/dataset-collection-LOW/edit/delete/dLu03X7K.mp3"  # Remplacez par le chemin de votre nouveau fichier vocal
new_mfccs = extract_mfcc(new_audio_path)
# Appliquer le même prétraitement que pour les données d'entraînement (padding, etc.)
new_data = pad_sequences([new_mfccs], dtype='float32', padding='post', maxlen=max_sequence_length)

# Faire des prédictions
predictions = model.predict(new_data.reshape(*new_data.shape, 1))

# Interpréter les résultats
predicted_class_index = np.argmax(predictions)
predicted_class = [key for key, value in label_to_index.items() if value == predicted_class_index]

print(f"Classe prédite : {predicted_class} en chiffre {predicted_class_index}")