import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras import layers, models
from keras.utils import to_categorical
from keras.preprocessing.sequence import pad_sequences


# Function to extract features from audio files
def extract_features(file_path):
    try:
        # Load audio file
        audio, _ = librosa.load(file_path, res_type='kaiser_fast')

        # Extract MFCC features
        mfccs = librosa.feature.mfcc(y=audio, sr=22050, n_mfcc=13)

        # Flatten the data
        flat_mfccs = np.ravel(mfccs)

    except Exception as e:
        print(f"Error while processing {file_path}: {e}")
        return None

    return flat_mfccs

# Function to load the dataset
def load_data(parent_folder):
    labels = []
    features = []

    for folder in os.listdir(parent_folder):
        child_folder = os.path.join(parent_folder, folder)

        if os.path.isdir(child_folder):
            for subfolder in os.listdir(child_folder):
                class_folder = os.path.join(child_folder, subfolder)

                if os.path.isdir(class_folder):
                    for filename in os.listdir(class_folder):
                        file_path = os.path.join(class_folder, filename)
                        feature = extract_features(file_path)

                        if feature is not None:
                            features.append(feature)
                            labels.append(subfolder)

    return np.array(features), np.array(labels)

# Define the path to your dataset
dataset_path = "/Users/abdelwahed/Desktop/dataset-collection-LOW/dataset-collection-LOW/"

# Load the dataset
features, labels = load_data(dataset_path)
print(labels)
# Encode labels
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)
num_classes = len(label_encoder.classes_)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, encoded_labels, test_size=0.2, random_state=42)

# Reshape the data for CNN input
# Ensure that X_train has a valid shape
print("Original shape of X_train:", X_train.shape)

# Reshape the data for CNN input
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))

# Ensure that X_train has the expected shape after reshaping
print("Shape of X_train after reshaping:", X_train.shape)
#X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))

X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
#X_train = pad_sequences(features, dtype='float32', padding='post')
#X_test =  pad_sequences(features, dtype='float32', padding='post')

# Convert labels to categorical
y_train = to_categorical(y_train, num_classes=num_classes)
y_test = to_categorical(y_test, num_classes=num_classes)

# Define the CNN model
model = models.Sequential()
model.add(layers.Conv1D(64, kernel_size=3, activation='relu', input_shape=(X_train.shape[1],1)))
model.add(layers.MaxPooling1D(pool_size=2))
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(num_classes, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy * 100:.2f}%")
