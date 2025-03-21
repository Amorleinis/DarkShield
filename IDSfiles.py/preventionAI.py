import joblib
import numpy as np
import logging
from datetime import datetime
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import load_model

# Configure logging
logging.basicConfig(filename='rnn_intrusion_detection.log', level=logging.INFO)

# Load and preprocess data


def load_data(filepath):
    try:
        data = pd.read_csv(filepath)
        return data
    except Exception as e:
        logging.error(f"Failed to load data from {filepath}: {e}")
        return None


def preprocess_data(data):
    features = data.drop('label', axis=1)
    labels = data['label']

    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    X = features_scaled.reshape(
        (features_scaled.shape[0], 1, features_scaled.shape[1]))
    y = labels.values

    return X, y

# Build the RNN model


def build_rnn_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, input_shape=input_shape, return_sequences=True))
    model.add(LSTM(50))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model

# Train the RNN model


def train_model(model, X_train, y_train, X_val, y_val):
    early_stopping = EarlyStopping(
        monitor='val_loss', patience=3, restore_best_weights=True)

    history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(
        X_val, y_val), callbacks=[early_stopping])
    return model, history

# Save the trained model


def save_model(model, model_path):
    model.save(model_path)
    logging.info(f"Model saved to {model_path}")

# Load the trained model


def load_trained_model(model_path):
    model = load_model(model_path)
    logging.info(f"Model loaded from {model_path}")
    return model

# Predict anomalies


def predict_anomalies(model, X):
    predictions = model.predict(X)
    return (predictions > 0.5).astype(int)


def main():
    # Load and preprocess data
    data_filepath = 'data/network_traffic.csv'  # Replace with your dataset path
    data = load_data(data_filepath)

    if data is None:
        logging.error("No data to process. Exiting.")
        return

    X, y = preprocess_data(data)

    # Split data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # Build and train the RNN model
    input_shape = (X_train.shape[1], X_train.shape[2])
    rnn_model = build_rnn_model(input_shape)
    rnn_model, history = train_model(rnn_model, X_train, y_train, X_val, y_val)

    # Save the trained model
    model_path = 'models/rnn_intrusion_detection_model.h5'
    save_model(rnn_model, model_path)

    # Load the trained model (for demonstration purposes)
    trained_model = load_trained_model(model_path)

# Predict anomalies on the validation set
    anomalies = predict_anomalies(trained_model, X_val)
    logging.info(
    f"Anomalies detected: {np.sum(anomalies)} out of {len(anomalies)}")

# Save detected anomalies to a file
output_file = f"detected_anomalies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
pd.DataFrame(anomalies, columns=['Anomaly']).to_csv(
    output_file, index=False)
logging.info(f"Detected anomalies saved to {output_file}")


if __name__ == "__main__":
    main()


class AIDetectionModel:
    def __init__(self, model_path=None):
        if model_path:
            self.model = joblib.load(model_path)
        else:
            self.model = make_pipeline(
                StandardScaler(),
                RandomForestClassifier(n_estimators=100, random_state=42)
            )

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        print("Model training completed.")

    def predict(self, data):
        if isinstance(data, dict):
            data = np.array([list(data.values())])
        return self.model.predict(data)

    def save_model(self, model_path):
        joblib.dump(self.model, model_path)
        print(f"Model saved to {model_path}")

    def update_model(self, X_new, y_new):
        self.model.fit(X_new, y_new)
        print("Model updated with new data.")


# Example usage
if __name__ == "__main__":
    # Sample data for training
    X_train = np.array([[0.1, 0.2, 0.3], [1.0, 1.1, 1.2], [0.5, 0.6, 0.7]])
    y_train = np.array([0, 1, 0])

    # Initialize and train the model
    ai_model = AIDetectionModel()
    ai_model.train(X_train, y_train)

    # Save the trained model
    ai_model.save_model("intrusion_detection_model.pkl")

    # Load the model and make a prediction
    loaded_model = AIDetectionModel(model_path="intrusion_detection_model.pkl")
    sample_data = {"feature1": 0.2, "feature2": 0.3, "feature3": 0.4}
    prediction = loaded_model.predict(sample_data)
    print(f"Prediction: {prediction}")
