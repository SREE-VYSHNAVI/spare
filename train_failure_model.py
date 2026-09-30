import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load telemetry dataset
df = pd.read_csv('1_telemetry_data.csv')

# Define features (sensors) and target (failure flag)
features = ['vibration_mm_s', 'bearing_temp_c', 'motor_current_a', 'pressure_bar']
X = df[features]
y = df['breakdown_flag']

# Split into 80% training and 20% testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train the Random Forest Classifier
clf_model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
clf_model.fit(X_train, y_train)

# Evaluate accuracy
predictions = clf_model.predict(X_test)
print("--- Failure Prediction Model ---")
print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")
print(classification_report(y_test, predictions))

# Export the trained model
joblib.dump(clf_model, 'failure_predictor.pkl')
print("Saved as 'failure_predictor.pkl'")