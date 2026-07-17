import os
import warnings
warnings.filterwarnings("ignore")

import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

# ---------------------------------------------------
# CREATE REQUIRED FOLDERS
# ---------------------------------------------------

os.makedirs("models", exist_ok=True)
os.makedirs("static", exist_ok=True)

# ---------------------------------------------------
# LOAD DATASET
# ---------------------------------------------------

DATA_PATH = "data/StudentPerformanceFactors.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("AI DRIVEN STUDENT PERFORMANCE PREDICTION SYSTEM")
print("=" * 70)

print("\nDataset Shape")
print(df.shape)

print("\nColumns")
print(df.columns.tolist())

print("\nMissing Values")
print(df.isnull().sum())

print("\nData Types")
print(df.dtypes)

print("\nStatistical Summary")
print(df.describe())

# ---------------------------------------------------
# TARGET COLUMN
# ---------------------------------------------------

TARGET = "Exam_Score"

# ---------------------------------------------------
# HANDLE MISSING VALUES
# ---------------------------------------------------

categorical_columns = df.select_dtypes(include="object").columns.tolist()

if TARGET in categorical_columns:
    categorical_columns.remove(TARGET)

numeric_columns = []

for col in df.columns:

    if col not in categorical_columns and col != TARGET:

        numeric_columns.append(col)

for col in categorical_columns:

    df[col] = df[col].fillna(df[col].mode()[0])

for col in numeric_columns:

    df[col] = df[col].fillna(df[col].median())

# ---------------------------------------------------
# LABEL ENCODING
# ---------------------------------------------------

encoders = {}

for col in categorical_columns:

    encoder = LabelEncoder()

    df[col] = encoder.fit_transform(df[col].astype(str))

    encoders[col] = encoder

# ---------------------------------------------------
# CORRELATION HEATMAP
# ---------------------------------------------------

plt.figure(figsize=(12,10))

corr = df.corr()

plt.imshow(corr, cmap="coolwarm")

plt.colorbar()

plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)

plt.yticks(range(len(corr.columns)), corr.columns)

plt.title("Correlation Heatmap")

plt.tight_layout()

plt.savefig("static/correlation_heatmap.png")

plt.close()

# ---------------------------------------------------
# TARGET DISTRIBUTION
# ---------------------------------------------------

plt.figure(figsize=(8,5))

plt.hist(df[TARGET], bins=30)

plt.title("Exam Score Distribution")

plt.xlabel("Exam Score")

plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig("static/target_distribution.png")

plt.close()

# ---------------------------------------------------
# FEATURES
# ---------------------------------------------------

X = df.drop(columns=[TARGET])

y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42

)

print("\nTraining Samples :", len(X_train))

print("Testing Samples :", len(X_test))

print("\nTraining Models...")


# ---------------------------------------------------
# MODEL DEFINITIONS
# ---------------------------------------------------

models = {

    "Linear Regression": LinearRegression(),

    "Decision Tree": DecisionTreeRegressor(
        random_state=42
    ),

    "Random Forest": RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        random_state=42
    )

}

results = []

best_model = None
best_name = ""
best_r2 = -999

# ---------------------------------------------------
# TRAIN & EVALUATE
# ---------------------------------------------------

for name, model in models.items():

    print(f"\nTraining {name}...")

    model.fit(X_train, y_train)

    prediction = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        prediction
    )

    mse = mean_squared_error(
        y_test,
        prediction
    )

    rmse = np.sqrt(mse)

    r2 = r2_score(
        y_test,
        prediction
    )

    results.append({

        "Model": name,

        "MAE": round(mae,3),

        "MSE": round(mse,3),

        "RMSE": round(rmse,3),

        "R2": round(r2,4)

    })

    print(f"MAE  : {mae:.3f}")
    print(f"MSE  : {mse:.3f}")
    print(f"RMSE : {rmse:.3f}")
    print(f"R2   : {r2:.4f}")

    if r2 > best_r2:

        best_r2 = r2

        best_model = model

        best_name = name

# ---------------------------------------------------
# BEST MODEL
# ---------------------------------------------------

print("\n" + "="*70)

print("BEST MODEL :", best_name)

print("R² SCORE   :", round(best_r2,4))

print("="*70)

metrics = pd.DataFrame(results)

metrics.to_csv(
    "models/metrics.csv",
    index=False
)

print("\nMetrics saved successfully.")

# ---------------------------------------------------
# FEATURE IMPORTANCE
# ---------------------------------------------------

if hasattr(best_model, "feature_importances_"):

    importance = pd.DataFrame({

        "Feature": X.columns,

        "Importance": best_model.feature_importances_

    })

    importance = importance.sort_values(

        by="Importance",

        ascending=False

    )

    importance.to_csv(

        "models/feature_importance.csv",

        index=False

    )

    plt.figure(figsize=(10,7))

    plt.barh(

        importance["Feature"],

        importance["Importance"]

    )

    plt.gca().invert_yaxis()

    plt.title("Feature Importance")

    plt.xlabel("Importance")

    plt.tight_layout()

    plt.savefig(

        "static/feature_importance.png"

    )

    plt.close()
    # ---------------------------------------------------
# ACTUAL vs PREDICTED GRAPH
# ---------------------------------------------------

best_prediction = best_model.predict(X_test)

plt.figure(figsize=(8,8))

plt.scatter(
    y_test,
    best_prediction,
    alpha=0.6
)

plt.plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    color="red",
    linewidth=2
)

plt.xlabel("Actual Exam Score")
plt.ylabel("Predicted Exam Score")
plt.title("Actual vs Predicted")
plt.tight_layout()

plt.savefig("static/actual_vs_predicted.png")

plt.close()

# ---------------------------------------------------
# SAVE MODEL FILES
# ---------------------------------------------------

joblib.dump(
    best_model,
    "models/model.pkl"
)

joblib.dump(
    encoders,
    "models/encoders.pkl"
)

joblib.dump(
    list(X.columns),
    "models/features.pkl"
)

# ---------------------------------------------------
# DISPLAY FEATURE IMPORTANCE
# ---------------------------------------------------

if hasattr(best_model, "feature_importances_"):

    print("\nTop 10 Important Features\n")

    print(importance.head(10))

# ---------------------------------------------------
# FINAL REPORT
# ---------------------------------------------------

print("\n" + "=" * 70)
print("PROJECT COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nBest Model")
print("--------------------------")
print(best_name)

print("\nModel Files")
print("--------------------------")
print("✔ models/model.pkl")
print("✔ models/encoders.pkl")
print("✔ models/features.pkl")
print("✔ models/metrics.csv")

print("\nGraphs Generated")
print("--------------------------")
print("✔ static/correlation_heatmap.png")
print("✔ static/target_distribution.png")
print("✔ static/feature_importance.png")
print("✔ static/actual_vs_predicted.png")

print("\nAccuracy Report")
print("--------------------------")

final_prediction = best_model.predict(X_test)

print(f"MAE  : {mean_absolute_error(y_test, final_prediction):.3f}")
print(f"MSE  : {mean_squared_error(y_test, final_prediction):.3f}")
print(f"RMSE : {np.sqrt(mean_squared_error(y_test, final_prediction)):.3f}")
print(f"R²   : {r2_score(y_test, final_prediction):.4f}")

print("\nThank you for using the AI Driven Student Performance Prediction System.")
print("=" * 70)