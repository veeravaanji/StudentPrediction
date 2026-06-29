from flask import Flask, render_template, request
import joblib
import sqlite3

app = Flask(__name__)

# Load model
model = joblib.load("model/model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    study_hours = float(request.form["study_hours"])
    attendance = float(request.form["attendance"])
    past_exam_score = float(request.form["past_exam_score"])

    # Default values for remaining features
    gender = 0
    parent_education = 0
    internet_access = 1
    extracurricular = 0

    prediction = model.predict([[
        gender,
        study_hours,
        attendance,
        past_exam_score,
        parent_education,
        internet_access,
        extracurricular
    ]])

    result = "Pass" if prediction[0] == 1 else "Fail"

    # Save into database
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions
    (gender,study_hours,attendance,past_exam_score,parent_education,internet_access,extracurricular,prediction)
    VALUES(?,?,?,?,?,?,?,?)
    """,(
        "Male",
        study_hours,
        attendance,
        past_exam_score,
        "Graduate",
        "Yes",
        "No",
        result
    ))

    conn.commit()
    conn.close()

    return render_template("index.html", prediction=result)


if __name__ == "__main__":
    app.run(debug=True)