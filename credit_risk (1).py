import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load the dataset from a CSV file
data = pd.read_csv('data.csv')

# Split the dataset into features (X) and labels (y)
X = data[['income', 'loan_amount', 'credit_score']].values  # Features
y = data['default'].values  # Target variable

# Split data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Evaluate the model's accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Predict the risk of default for a new customer
new_customer = np.array([[75000, 28000, 710]])  # Example customer data
default_prediction = model.predict(new_customer)
print("Default risk:", "Yes" if default_prediction == 1 else "No")

