from flask import Flask, render_template, request
import pandas as pd
import joblib
import traceback

# ----------------------------------------------------
# LOAD APPLICATION
# ----------------------------------------------------

app = Flask(__name__)

# ----------------------------------------------------
# LOAD TRAINED FILES
# ----------------------------------------------------

model = joblib.load("models/model.pkl")
encoders = joblib.load("models/encoders.pkl")
features = joblib.load("models/features.pkl")

# ----------------------------------------------------
# HOME PAGE
# ----------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")

# ----------------------------------------------------
# PREDICTION
# ----------------------------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = {}

        # ---------------------------------------------
        # READ ALL FEATURES
        # ---------------------------------------------

        for feature in features:

            value = request.form.get(feature)

            if feature in encoders:

                value = encoders[feature].transform([value])[0]

            else:

                value = float(value)

            data[feature] = value

        input_df = pd.DataFrame([data])

        prediction = round(model.predict(input_df)[0],2)

        # ---------------------------------------------
        # PERFORMANCE CATEGORY
        # ---------------------------------------------

        if prediction >= 90:

            category = "Outstanding"

            emoji = "🏆"

            color = "#16a34a"

        elif prediction >= 75:

            category = "Excellent"

            emoji = "⭐"

            color = "#2563eb"

        elif prediction >= 60:

            category = "Good"

            emoji = "👍"

            color = "#f59e0b"

        elif prediction >= 40:

            category = "Average"

            emoji = "📘"

            color = "#fb923c"

        else:

            category = "Needs Improvement"

            emoji = "⚠️"

            color = "#dc2626"

        # ---------------------------------------------
        # RISK LEVEL
        # ---------------------------------------------

        if prediction >= 75:

            risk = "LOW"

        elif prediction >= 50:

            risk = "MEDIUM"

        else:

            risk = "HIGH"

        # ---------------------------------------------
        # AI RECOMMENDATIONS
        # ---------------------------------------------

        suggestions = []

        if data["Attendance"] < 75:
            suggestions.append("Increase attendance above 75%.")

        if data["Hours_Studied"] < 4:
            suggestions.append("Study at least 4–6 hours daily.")

        if data["Sleep_Hours"] < 7:
            suggestions.append("Maintain 7–8 hours of sleep.")

        if data["Tutoring_Sessions"] < 2:
            suggestions.append("Attend additional tutoring sessions.")

        if data["Previous_Scores"] < 70:
            suggestions.append("Revise previous concepts regularly.")

        if data["Physical_Activity"] < 1:
            suggestions.append("Engage in regular physical activity.")

        if len(suggestions) == 0:
            suggestions.append("Excellent habits! Keep maintaining your performance.")

        # ----------------------------------------------------
        # RETURN RESULTS
        # ----------------------------------------------------

        return render_template(

            "index.html",

            prediction=prediction,

            category=category,

            emoji=emoji,

            color=color,

            risk=risk,

            suggestions=suggestions,

            feature_graph="feature_importance.png",

            correlation_graph="correlation_heatmap.png",

            distribution_graph="target_distribution.png",

            prediction_graph="actual_vs_predicted.png"

        )

    # ----------------------------------------------------
    # ERROR HANDLING
    # ----------------------------------------------------

    except Exception as e:

        print(traceback.format_exc())

        return render_template(

            "index.html",

            error=str(e)

        )


# ----------------------------------------------------
# RUN APPLICATION
# ----------------------------------------------------

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )