import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error
import joblib

# Load supply chain history
df = pd.read_csv('6_supply_chain_history.csv')

# Define features (text categories) and target (actual delivery days)
X = df[['part_no', 'season', 'market_condition']]
y = df['actual_delivery_days']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create an encoder to convert text labels into numeric data
categorical_features = ['part_no', 'season', 'market_condition']
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

preprocessor = ColumnTransformer(transformers=[
    ('cat', categorical_transformer, categorical_features)
])

# Build a pipeline that encodes the data, then trains the regressor
reg_model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train the model
reg_model.fit(X_train, y_train)

# Evaluate the error margin
predictions = reg_model.predict(X_test)
print("\n--- Supply Chain Prediction Model ---")
error = mean_absolute_error(y_test, predictions)
print(f"Average Error Margin: +/- {error:.2f} days")

# Export the trained pipeline
joblib.dump(reg_model, 'supply_chain_predictor.pkl')
print("Saved as 'supply_chain_predictor.pkl'")