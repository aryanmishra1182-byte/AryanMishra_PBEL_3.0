# 🎓 EduPredict AI – Student Performance Prediction System

An end-to-end Machine Learning web application that predicts a student's academic performance based on study habits, attendance, and lifestyle factors.

---

## 🚀 Live Demo

### 🌐 Frontend
https://stunning-starlight-6d53bb.netlify.app/

### 🤖 Backend API
https://aryanmishra-pbel-3-0-1.onrender.com

---

# 📌 Project Overview

EduPredict AI is a Machine Learning-powered web application that predicts a student's academic performance using educational and lifestyle parameters.

The application combines a trained Machine Learning model with a Flask REST API and a modern responsive frontend to provide instant predictions along with personalized recommendations.

---

# ✨ Features

- 🎯 AI-based Student Performance Prediction
- 📊 Interactive Prediction Form
- ⚡ Real-time Prediction
- 📈 Performance Score Visualization
- 💡 Personalized Recommendations
- 📱 Responsive UI
- 🔗 REST API Support
- ☁️ Cloud Deployment
- 🤖 Machine Learning Integration

---

# 🛠 Tech Stack

## Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap

## Backend
- Python
- Flask
- Flask-CORS

## Machine Learning
- Scikit-Learn
- Pandas
- NumPy
- Joblib

## Deployment
- Netlify
- Render

---

# 🧠 Machine Learning Workflow

```
Dataset
   │
   ▼
Data Cleaning
   │
   ▼
Feature Engineering
   │
   ▼
Categorical Encoding
   │
   ▼
Model Training
   │
   ▼
Model Evaluation
   │
   ▼
Model Serialization (.pkl)
   │
   ▼
Flask API
   │
   ▼
Netlify Frontend
```

---

# 📂 Project Structure

```
EduPredict-AI
│
├── app.py
├── requirements.txt
├── models/
│   ├── model.pkl
│   ├── encoders.pkl
│   └── features.pkl
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── README.md
```

---

# 🔗 API Endpoint

### POST Request

```
POST /api/predict
```

### Sample Request

```json
{
  "attendance": 85,
  "study_hours": 5,
  "sleep_hours": 7,
  "previous_grade": 82
}
```

### Sample Response

```json
{
  "prediction": "Excellent",
  "score": 91.42,
  "recommendation": "Maintain your current study routine."
}
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/aryanmishra1182-byte/AryanMishra_PBEL_3.0.git
```

Move into the project directory

```bash
cd AryanMishra_PBEL_3.0
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

---

# 🌍 Deployment

### Frontend
Netlify

### Backend
Render

---

# 🚀 Future Improvements

- User Authentication
- Prediction History
- Student Dashboard
- Data Analytics
- Charts & Graphs
- PDF Report Generation
- Explainable AI (SHAP)
- Database Integration

---

# 📸 Screenshots

> Add screenshots of your application here.

- Home Page
- Prediction Form
- Prediction Result
- Recommendation Section

---

# 👨‍💻 Author

**Aryan Mishra**

B.Tech CSE (Data Science)  
ABES Engineering College

GitHub:
https://github.com/aryanmishra1182-byte

---

# ⭐ Support

If you found this project helpful, please ⭐ star this repository.

It motivates me to build more Machine Learning and AI projects.

---

## 📄 License

This project is developed for educational purposes and learning Machine Learning deployment using Flask, Render, and Netlify.