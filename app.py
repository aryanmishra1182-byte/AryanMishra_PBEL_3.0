from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# ==========================
# LOAD FILES
# ==========================

model = joblib.load("models/model.pkl")
encoders = joblib.load("models/encoders.pkl")
features = joblib.load("models/features.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    data = {
        "Hours_Studied": float(request.form["Hours_Studied"]),
        "Attendance": float(request.form["Attendance"]),
        "Parental_Involvement": request.form["Parental_Involvement"],
        "Access_to_Resources": request.form["Access_to_Resources"],
        "Extracurricular_Activities": request.form["Extracurricular_Activities"],
        "Sleep_Hours": float(request.form["Sleep_Hours"]),
        "Previous_Scores": float(request.form["Previous_Scores"]),
        "Motivation_Level": request.form["Motivation_Level"],
        "Internet_Access": request.form["Internet_Access"],
        "Tutoring_Sessions": float(request.form["Tutoring_Sessions"]),
        "Family_Income": request.form["Family_Income"],
        "Teacher_Quality": request.form["Teacher_Quality"],
        "School_Type": request.form["School_Type"],
        "Peer_Influence": request.form["Peer_Influence"],
        "Physical_Activity": float(request.form["Physical_Activity"]),
        "Learning_Disabilities": request.form["Learning_Disabilities"],
        "Parental_Education_Level": request.form["Parental_Education_Level"],
        "Distance_from_Home": request.form["Distance_from_Home"],
        "Gender": request.form["Gender"]
    }

    df = pd.DataFrame([data])

    # ==========================
    # LABEL ENCODING
    # ==========================

    for col, encoder in encoders.items():

        df[col] = encoder.transform(df[col].astype(str))

    # feature order same as training

    df = df[features]

    prediction = float(model.predict(df)[0])

    prediction = round(prediction, 2)

    if prediction < 0:
        prediction = 0

    if prediction > 100:
        prediction = 100

    # ==========================
    # RESULT
    # ==========================

    if prediction >= 85:

        performance = "🌟 Outstanding Performance"
        risk = "Very Low"
        color = "#22c55e"

        recommendations = [
            "Maintain your excellent consistency.",
            "Participate in coding contests & hackathons.",
            "Keep solving advanced problems.",
            "Continue balancing academics and health.",
            "Help classmates through peer learning."
        ]

    elif prediction >= 70:

        performance = "✅ Good Performance"
        risk = "Low"
        color = "#38bdf8"

        recommendations = [
            "Practice weak subjects regularly.",
            "Increase revision frequency.",
            "Maintain attendance above 90%.",
            "Solve previous year papers.",
            "Continue your current routine."
        ]

    elif prediction >= 50:

        performance = "⚠ Average Performance"
        risk = "Medium"
        color = "#f59e0b"

        recommendations = [
            "Increase daily study hours.",
            "Reduce distractions.",
            "Take help from teachers.",
            "Prepare weekly goals.",
            "Improve attendance."
        ]

    else:

        performance = "❌ Needs Improvement"
        risk = "High"
        color = "#ef4444"

        recommendations = [
            "Follow a strict timetable.",
            "Study every day.",
            "Revise basic concepts.",
            "Seek mentorship.",
            "Avoid procrastination."
        ]

    return render_template(

        "index.html",

        prediction=prediction,
        performance=performance,
        risk=risk,
        color=color,
        recommendations=recommendations

    )


@app.errorhandler(404)
def not_found(e):
    return render_template("index.html"), 404


@app.errorhandler(500)
def internal(e):
    return render_template("index.html"), 500

@app.route("/api/predict", methods=["POST"])
def api_predict():

    data = request.get_json()

    df = pd.DataFrame([data])

    for col, encoder in encoders.items():
        df[col] = encoder.transform(df[col].astype(str))

    df = df[features]

    prediction = float(model.predict(df)[0])
    prediction = max(0, min(100, round(prediction, 2)))

    if prediction >= 85:
        performance = "🌟 Outstanding Performance"
        risk = "Very Low"
        color = "#22c55e"
        recommendations = [
            "Maintain your excellent consistency.",
            "Participate in coding contests & hackathons.",
            "Keep solving advanced problems.",
            "Continue balancing academics and health.",
            "Help classmates through peer learning."
        ]

    elif prediction >= 70:
        performance = "✅ Good Performance"
        risk = "Low"
        color = "#38bdf8"
        recommendations = [
            "Practice weak subjects regularly.",
            "Increase revision frequency.",
            "Maintain attendance above 90%.",
            "Solve previous year papers.",
            "Continue your current routine."
        ]

    elif prediction >= 50:
        performance = "⚠ Average Performance"
        risk = "Medium"
        color = "#f59e0b"
        recommendations = [
            "Increase daily study hours.",
            "Reduce distractions.",
            "Take help from teachers.",
            "Prepare weekly goals.",
            "Improve attendance."
        ]

    else:
        performance = "❌ Needs Improvement"
        risk = "High"
        color = "#ef4444"
        recommendations = [
            "Follow a strict timetable.",
            "Study every day.",
            "Revise basic concepts.",
            "Seek mentorship.",
            "Avoid procrastination."
        ]

    return jsonify({
        "prediction": prediction,
        "performance": performance,
        "risk": risk,
        "color": color,
        "recommendations": recommendations
    })
if __name__ == "__main__":
    app.run(debug=True)