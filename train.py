import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print(os.getcwd())

# Load dataset
df = pd.read_csv("dataset/student_performance_dataset.csv")

print("First 5 rows:")
print(df.head())

# Remove Student_ID (not useful for prediction)
df = df.drop("Student_ID", axis=1)

# Convert categorical columns into numbers
encoder = LabelEncoder()

categorical_columns = [
    "Gender",
    "Parental_Education_Level",
    "Internet_Access_at_Home",
    "Extracurricular_Activities",
    "Pass_Fail"
]

for col in categorical_columns:
    df[col] = encoder.fit_transform(df[col])

print("\nConverted Dataset:")
print(df.head())

# Features (Input)
X = df.drop(["Final_Exam_Score", "Pass_Fail"], axis=1)

# Target (Output)
y = df["Pass_Fail"]
print("Training features:")
print(X.columns)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create model
model = RandomForestClassifier(random_state=42)

# Train model
model.fit(X_train,y_train)

# Prediction
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test,y_pred)

print("\nAccuracy:",accuracy)
import joblib

joblib.dump(model, "model/model.pkl")

print("Model saved successfully!")