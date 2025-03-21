import numpy as np
import joblib
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.datasets import make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

class MachineLearningAI:

    def __init__(self, classifier=None, param_grid=None):
        self.classifier = classifier if classifier is not None else MLPClassifier()
        self.param_grid = param_grid
        self.pipeline = None
        self.grid_search = None
        self.best_params = None
        self.best_score = None


    def generate_dataset(self, n_samples=100, n_features=20, test_size=0.25, random_state=42):
        X, y = make_classification(n_samples=n_samples, n_features=n_features, n_informative=2, n_classes=2, random_state=random_state)
        return train_test_split(X, y, test_size=test_size, random_state=random_state)

    def configure_pipeline(self, steps):
        self.pipeline = Pipeline(steps)

    def generate_and_train_classifier(self, X_train, y_train, cv=5):
        if self.pipeline is None:

          self.configure_pipeline([('scaler', StandardScaler()), ('poly', PolynomialFeatures()), ('classifier', self.classifier)])
        if self.param_grid is not None:
            self.grid_search = GridSearchCV(self.pipeline,
                        self.param_grid, cv=cv, n_jobs=-1)
            self.grid_search.fit(X_train, y_train)
            print(f'Best parameters found: {self.grid_search.best_params_}')
            self.best_params = self.grid_search.best_params_
            self.pipeline = self.grid_search.best_estimator_
        else:
            scores = cross_val_score(self.pipeline, X_train, y_train, cv=cv, n_jobs=-1)
            self.pipeline.fit(X_train, y_train)
            return np.mean(scores)

    def evaluate_classifier(self, X_test, y_test):
        y_pred = self.pipeline.predict(X_test)
        print(classification_report(y_test, y_pred))
        print(confusion_matrix(y_test, y_pred))
        return accuracy_score(y_test, y_pred)

    def save_model(self, filename):
        joblib.dump(self.pipeline, filename)
        print(f'Model saved to {filename}')

    def load_model(self, filename):
        self.pipeline = joblib.load(filename)
        print(f'Model loaded from {filename}')

# Set up classifiers and parameter grids to use
classifier_params = {
    'MLP': (MLPClassifier(), {
        'classifier__hidden_layer_sizes': [(50,), (100,)],
        'classifier__activation': ['tanh', 'relu', 'logistic',],
        'classifier__solver': ['sgd', 'adam', 'lbfgs'],
        'classifier__alpha': [0.0001, 0.05],
        'classifier__learning_rate': ['constant','adaptive', 'invscaling'],
        'classifier__learning_rate_init': [0.001, 0.01, 0.1],
        'classifier__max_iter': [100, 1000],
        'classifier__momentum': [0.9, 0.99],
        'classifier__nesterovs_momentum': [True, False],
        'classifier__early_stopping': [True, False],
        'classifier__validation_fraction': [0.1, 0.2],
        'classifier__beta_1': [0.9, 0.99],
        'classifier__beta_2': [0.9, 0.99],
        'classifier__epsilon': [1e-08, 1e-07],
        'classifier__n_iter_no_change': [10, 20, 30],
    }),
    'Decision Tree': (DecisionTreeClassifier(), {
        'classifier__max_depth': [None, 10, 20, 30],
        'classifier__min_samples_split': [2, 5, 10],
        'classifier__min_samples_leaf': [1, 2, 4],
        'classifier__min_weight_fraction_leaf': [0.0, 0.1, 0.2],
        'classifier__criterion': ['gini', 'entropy']
    }),
    'Random Forest': (RandomForestClassifier(), {
        'classifier__n_estimators': [50, 100, 200],
        'classifier__max_features': ['auto', 'sqrt', 'log2'],
        'classifier__max_depth': [None, 5, 10, 15, 20],
        'classifier__min_samples_split': [2, 5, 10],
    }),
    'SVM': (SVC(), {
        'classifier__C': [0.1, 1, 10],
        'classifier__gamma': ['scale', 'auto', 0.001, 0.01, 0.1, 1],
        'classifier__kernel': ['linear', 'rbf', 'poly', 'sigmoid'],
    }),
    'Logistic Regression': (LogisticRegression(), {
        'classifier__C': [0.1, 1, 10, 100],
        'classifier__penalty': ['l1', 'l2'],
        'classifier__solver': ['adam', 'newton-cg', 'lbfgs', 'liblinear' 'sag', 'saga'],
    }),
}

def save_best_models(classifier_params):
    for name, (clf, params) in classifier_params.items():
        print(f'\nTraining and evaluating {name}')
        ai = MachineLearningAI(classifier=clf, param_grid=params)
        X_train, X_test, y_train, y_test = ai.generate_dataset()

        ai.generate_and_train_classifier(X_train, y_train)
        accuracy = ai.evaluate_classifier(X_test, y_test)
        print(f'{name} Model Accuracy: {accuracy}')

        # Save the best model
        model_file = f'best_{name.lower().replace(" ", "_")}_model.joblib'
        ai.save_model(model_file)


# Call the function to save the best models
save_best_models(classifier_params)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping


class DeepLearningAI(MachineLearningAI):

    def __init__(self, classifier=None, param_grid=None):
        super().__init__(classifier, param_grid)

    def configure_deep_learning_model(self, input_dim):
        self.classifier = Sequential([
            Dense(128, input_dim=input_dim, activation='relu'),
            Dense(64, activation='relu'),
            Dense(32, activation='relu'),
            Dense(1, activation='sigmoid'),
        ])
        self.classifier.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

    def train_deep_learning_model(self, X_train, y_train, epochs=10240, batch_size=10):
        self.classifier.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)

    def evaluate_deep_learning_model(self, X_test, y_test):
        evaluation = self.classifier.evaluate(X_test, y_test)
        return evaluation

# Integration into the existing workflow
def train_and_save_deep_learning_model():
    ai = DeepLearningAI()
    X_train, X_test, y_train, y_test = ai.generate

ai.configure_deep_learning_model(input_dim=20)
ai.train_deep_learning_model(X_train, y_train, epochs=10240, batch_size=10)
accuracy = ai.evaluate_deep_learning_model(X_test, y_test)
print

evaluation = ai.evaluate_deep_learning_model(X_test, y_test)
print(f'Deep Learning Model Accuracy: {evaluation[1]}')

    # Save the deep learning model
model_file = 'deep_learning_model.h5'
ai.classifier.save(model_file)
print(f'Model saved to {model_file}')

# Call the function to train and save the deep learning model
train_and_save_deep_learning_model()


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report

# Load pre-labeled network traffic data (features and whether traffic was normal or an attack/anomaly)
network_data = pd.read_csv('network_traffic_data.csv')

# Features in the dataset
X = network_data.drop('label', axis=1)  # 'label' column has the anomaly labels
# Labels (0 for normal traffic, 1 for anomaly/attack)
y = network_data['label']

# Split dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Initialize the model
model = RandomForestClassifier(n_estimators=100, random_state=0)

# Train the model
model.fit(X_train, y_train)

# Predict on test data
y_pred = model.predict(X_test)

# Evaluate the model
cm = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred)
print("Confusion Matrix:")
print(cm)
print("Classification Report:")
print(report)

def chat_with_model(model, X_test):
    print("Chat with the model:")
    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == 'exit':
            print("Model Chat: Goodbye! See you later!")
            break

        # Process user input (you might need to preprocess the input based on the model input requirements)
        user_input_features = process_user_input(user_input)

        # Use the model to predict a response
        model_response = model.predict(user_input_features)

        print("Model Chat:", model_response)

        def process_user_input(user_input):
            # Perform any necessary preprocessing on the user input to convert it into features for the model
            # This might involve tokenization, encoding, feature extraction, etc.
            # Return the processed features
            processed_input = preprocess_user_input(user_input)
            return processed_input