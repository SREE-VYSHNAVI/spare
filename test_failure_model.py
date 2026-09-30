import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# 1. Load your telemetry dataset
df = pd.read_csv('1_telemetry_data.csv')

# 2. Define features (sensors) and target (breakdown flag)
features = ['vibration_mm_s', 'bearing_temp_c', 'motor_current_a', 'pressure_bar']
X = df[features]
y = df['breakdown_flag']

# 3. Use 5-Fold Cross-Validation for a realistic performance check
# This splits your data 5 different ways to see how the model generalizes
model = RandomForestClassifier(n_estimators=100, random_state=42)
cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

print("--- Cross-Validation Evaluation ---")
print(f"Accuracy across 5 folds: {[round(score * 100, 2) for score in cv_scores]}")
print(f"Mean Accuracy: {cv_scores.mean() * 100:.2f}% (+/- {cv_scores.std() * 100:.2f}%)")

# 4. Final Train-Test Split to train and save the production model file
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model.fit(X_train, y_train)
predictions = model.predict(X_test)

print("\n--- Final Test Set Classification Report ---")
print(classification_report(y_test, predictions))

# 5. Save the trained model for your backend
joblib.dump(model, 'failure_predictor.pkl')
print("\nModel trained, evaluated with cross-validation, and saved as 'failure_predictor.pkl'")