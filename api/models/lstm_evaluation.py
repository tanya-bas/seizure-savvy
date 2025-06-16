
#lstm_evaluation
from tensorflow.keras.models import load_model

from lstm_model import get_split_dataset

# Load the model
model_loaded = load_model('lstm_model.h5')

X_train, X_test, y_train, y_test = get_split_dataset()

test_loss, test_accuracy = model_loaded.evaluate(X_test, y_test, verbose=2)
print(f"Test Loss: {test_loss}")
print(f"Test Accuracy: {test_accuracy}")

predictions = model_loaded.predict(X_test, verbose=2)
binary_predictions = (predictions > 0.5).astype(int)

# compare some predictions with actual values
for i in range(10):
    print(f"Predicted: {binary_predictions[i]}, Actual: {y_test[i]}")
