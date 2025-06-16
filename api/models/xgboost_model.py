import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from base_data import get_fake_dataset


#load the data
fake_dataset = get_fake_dataset()

# Define features and target
X = fake_dataset.drop('Episodes Occurrences', axis=1)
y = fake_dataset['Episodes Occurrences'].astype(int)  # Ensure target is integer

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the XGBoost model
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

# Predictions and evaluation
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy}")


#xgboost provides its own method for saving models
model.save_model('xgboost_model.json')
