from flask import Flask, render_template, request, redirect, url_for, session
import joblib
import sqlite3
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.secret_key = "studentprediction"

# Load trained model
model = joblib.load("model/model.pkl")


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")


# ---------------- PREDICTION PAGE ----------------
@app.route("/prediction")
def prediction():
    return render_template("index.html")


# ---------------- PREDICT ----------------
@app.route("/predict", methods=["GET", "POST"])
def predict():

    if request.method == "GET":
        # prevents Method Not Allowed error if page opened directly
        return redirect(url_for("prediction"))

    try:
        # Student Details
        student_name = request.form.get("student_name")
        student_id = request.form.get("student_id")

# Input Values
        gender = request.form.get("gender")
        study_hours = float(request.form.get("study_hours"))
        attendance = float(request.form.get("attendance"))
        sleep_hours = float(request.form.get("sleep_hours"))
        internet_access = request.form.get("internet_access")
        past_exam_score = float(request.form.get("past_exam_score"))
        extracurricular = request.form.get("extracurricular")


# Encode values
        gender = 1 if gender == "Male" else 0
        internet_access = 1 if internet_access == "Yes" else 0
        extracurricular = 1 if extracurricular == "Yes" else 0
        internet_access = 1 if internet_access == "Yes" else 0

# Create DataFrame
        input_data = pd.DataFrame([{
        "Gender": gender,
    "Study_Hours_per_Week": study_hours,
    "Attendance_Percentage": attendance,
    "Sleep_Hours_Per_Night": sleep_hours,
    "Internet_Access_at_Home": internet_access,
    "Previous_Exam_Score": past_exam_score,
    "Extracurricular_Activities": extracurricular
}])

        

        # Prediction
        prediction_result = model.predict(input_data)
        probability = model.predict_proba(input_data)

        confidence = round(max(probability[0]) * 100, 2)
        result = "Pass" if prediction_result[0] == 1 else "Fail"

        # Suggestion
        if result == "Pass":
            suggestion = "Excellent! Keep studying regularly."
        else:
            suggestion = "Increase study hours and attendance."

        # Date & Time
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        time = now.strftime("%I:%M %p")

        # Save to database
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()

        cursor.execute("""
    INSERT INTO predictions (
        student_name,
        student_id,
        gender,
        study_hours,
        attendance,
        sleep_hours,
        past_exam_score,
        internet_access,
        extracurricular,
        prediction,
        confidence,
        date,
        time
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    student_name,
    student_id,
    "Male" if gender == 1 else "Female",
    study_hours,
    attendance,
    sleep_hours,
    past_exam_score,
    "Yes" if internet_access == 1 else "No",
    "Yes" if extracurricular == 1 else "No",
    result,
    confidence,
    date,
    time
))

        conn.commit()
        conn.close()

        print("Prediction:", result)
        print("Confidence:", confidence)

        return render_template(

    "index.html",

    prediction=result,

    confidence=confidence,

    suggestion=suggestion,

    study_hours=study_hours,

    attendance=attendance,

    sleep_hours=sleep_hours,

    past_exam_score=past_exam_score,

    extracurricular=request.form.get("extracurricular")

)
    except Exception as e:
        return f"Error: {str(e)}"


# ---------------- ABOUT ----------------
@app.route("/about")
def about():
    return render_template("about.html")


# ---------------- ADMIN LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect(url_for("history"))

        return render_template("login.html", error="Invalid Username or Password")

    return render_template("login.html")


# ---------------- HISTORY ----------------
@app.route("/history")
def history():

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions")
    rows = cursor.fetchall()

    conn.close()

    return render_template("history.html", rows=rows)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)