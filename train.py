import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

# --------------------------------------------------
# Current Working Directory
# --------------------------------------------------
print("Current Directory:", os.getcwd())

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
df = pd.read_csv(r"C:\Users\ELCOT\Downloads\student_performance_dataset_5000.csv")

print(df.columns.tolist())

print(df.isnull().sum())
df = df.dropna()

print("\nFirst 5 Rows:")
print(df.head())

# --------------------------------------------------
# Remove Student_ID
# --------------------------------------------------
df.drop("Student_ID", axis=1, inplace=True)

# --------------------------------------------------
# Encode Categorical Columns
# --------------------------------------------------
categorical_columns = [
    "Gender",
   "Sleep_Hours_Per_Night",
    "Internet_Access_at_Home",
    "Extracurricular_Activities",
    "Pass_Fail"
]

encoders = {}

for col in categorical_columns:
    encoder = LabelEncoder()
    df[col] = encoder.fit_transform(df[col])
    encoders[col] = encoder

print("\nConverted Dataset:")
print(df.head())

# --------------------------------------------------
# Input Features (X)
# --------------------------------------------------
X = df.drop(["Final_Exam_Score", "Pass_Fail"], axis=1)

# --------------------------------------------------
# Target (y)
# --------------------------------------------------
y = df["Pass_Fail"]

print("\nTraining Features:")
print(X.columns)

# --------------------------------------------------
# Split Dataset
# --------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# --------------------------------------------------
# Create Random Forest Model
# --------------------------------------------------
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    max_features="sqrt",
    random_state=42,
    n_jobs=-1
)

# --------------------------------------------------
# Train Model
# --------------------------------------------------
model.fit(X_train, y_train)

# --------------------------------------------------
# Prediction
# --------------------------------------------------
y_pred = model.predict(X_test)

# --------------------------------------------------
# Accuracy
# --------------------------------------------------
accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", accuracy)

# --------------------------------------------------
# Confusion Matrix
# --------------------------------------------------
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# --------------------------------------------------
# Classification Report
# --------------------------------------------------
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# --------------------------------------------------
# Feature Importance
# --------------------------------------------------
importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance:")
print(importance)

# --------------------------------------------------
# Save Model
# --------------------------------------------------
joblib.dump(model, "model/model.pkl")

print("\nModel saved successfully!")