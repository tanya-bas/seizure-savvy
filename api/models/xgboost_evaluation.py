import xgboost as xgb
from base_data import get_fake_dataset

fake_dataset = get_fake_dataset()
X = fake_dataset.drop('Episodes Occurrences', axis=1)

# Create an XGBoost model instance
model2 = xgb.XGBClassifier()

# Load the model from the file
model2.load_model('xgboost_model.json')

importance = model2.feature_importances_

# Summarize feature importance
for i, v in enumerate(importance):
    print(f'Feature: {X.columns[i]}, Score: {v}')

# Plot feature importance
xgb.plot_importance(model2)

