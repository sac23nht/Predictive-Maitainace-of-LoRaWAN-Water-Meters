# 💧 IoT Meter Connectivity Risk Prediction

## 📖 Overview
This project focuses on analyzing and predicting the **connectivity performance** of a fleet of smart water meters.  
The goal is to identify factors influencing the **Data Success Rate (DSR)** and build predictive models to flag meters at risk of failing to meet the **Key Performance Indicator (KPI)** of ≥ 85% DSR.

A **Streamlit web application** is included to provide an interactive interface for predicting meter risk using trained machine learning models.

---

## 🎯 Business Problem
A significant portion of smart water meters are failing to meet the required **Data Success Rate (DSR)** of 85%.  
This project aims to:

- 🔍 **Identify Key Risk Factors:** Determine which environmental and network factors (signal strength, distance to gateway, installation depth, etc.) most significantly impact meter performance.  
- 🤖 **Predict At-Risk Meters:** Develop a machine learning model to predict the probability of a meter falling below the 85% DSR threshold.  
- 💡 **Provide Actionable Insights:** Use the model’s predictions to proactively identify and address issues with at-risk meters, improving overall network reliability and reducing maintenance costs.

---

## 🚀 Getting Started

### 🧩 Prerequisites
- Python 3.8+
- Pip package manager

### ⚙️ Installation

Clone the repository:
```bash
git clone https://github.com/sac23nht/Predictive-Maitainace-of-LoRaWAN-Water-Meters.git
cd Predictive-Maitainace-of-LoRaWAN-Water-Meters
```

Create and activate a virtual environment:
``` bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
Install dependencies:
``` bash
pip install -r requirements.txt

```
▶️ Running the Application

Once the dependencies are installed, run the Streamlit web application:
``` bash
streamlit run app.py
```
📂 Project Structure

``` bash
├── app.py                                       # Entry point (runs src/main.py)
├── src/
│   ├── main.py                                  # Streamlit application code
│   ├── logistic_regression_pipeline.pkl         # Trained Logistic Regression Model
│   ├── random_forest_best_pipeline.pkl          # Trained Random Forest Model
│   └── xgboost_best_pipeline.pkl                # Trained XGBoost Model
│
├── data/
│   ├── Raw Data set.xlsx                        # Raw dataset
│   └── Test Data.xlsx                           # Test dataset
│
├── notebooks/
│   ├── Exploratory_Data_Analysis.ipynb          # EDA notebook
│   ├── Logistic_Regression.ipynb
│   ├── Random_FOrest.ipynb
│   └── XGBoost_Classifier.ipynb
│
├── requirements.txt                             # Python dependencies
├── runtime.txt                                  # Python version pin (Streamlit Cloud)
├── Dockerfile                                   # Container image for generic hosting
└── README.md                                    # This README file
```

---

## ☁️ Deployment

Model paths in the app are resolved relative to `src/main.py`, so no code
changes are needed to deploy elsewhere — just make sure the `.pkl` files in
`src/` are included.

### Option A — Streamlit Community Cloud
1. Push this repo to GitHub (already done if you're reading this there).
2. Go to [share.streamlit.io](https://share.streamlit.io), create a new app,
   point it at this repo and set the main file path to `app.py`.
3. Streamlit Cloud installs `requirements.txt` and uses `runtime.txt`
   automatically.

### Option B — Any Docker-based host (Render, Railway, Fly.io, a VPS, etc.)
```bash
docker build -t meter-risk-app .
docker run -p 8501:8501 meter-risk-app
```
The container reads the `$PORT` environment variable if the platform sets
one (Render/Railway do this automatically), otherwise it defaults to 8501.
🤖 Modeling
🎯 Target Variable

The models classify whether a meter is “At Risk” based on its DSR:

Label	Condition	Description
1	DSR% < 85	At Risk
0	DSR% ≥ 85	Safe
🧠 Models Implemented

Logistic Regression: Simple, interpretable baseline model.

Random Forest: Ensemble model with good balance between performance and interpretability.

XGBoost: Gradient boosting model known for high predictive accuracy.

🔑 Key Features

RSSI_dBm: Signal strength — lower values → higher risk.

SNR_dB: Signal-to-noise ratio — weaker signals → higher risk.

LidType: Cast Iron lids significantly reduce connectivity performance.

DistanceToNearestGateway_m: Greater distances reduce DSR.

Depth_mm: Deeper installations show higher connectivity risk.

📊 Key Findings from EDA

DSR Distribution: Bimodal — clusters below 20% and above 90%.

Signal Quality Matters: RSSI and SNR are the most influential predictors.

Installation Factors:

Lid Type: Cast Iron → poor DSR.

Depth: Greater depth → higher risk.

Distance: Increased distance → reduced DSR.

💻 How the App Works

Select a Model: Choose between Logistic Regression, Random Forest, or XGBoost.

Choose a Prediction Mode:

🟢 Default: Standard 0.5 probability threshold.

🔵 Recall-Focused: Lower threshold to catch more potential at-risk meters.

🟠 Precision-Focused: Higher threshold to minimize false alarms.

Enter Feature Values: Adjust sliders/dropdowns to input meter characteristics.

Predict: Click “Predict” to see whether the meter is AT RISK or SAFE, along with its probability score.

📦 Deliverables

📝 Written Report: Summary of analysis, model performance, and recommendations.

💻 Code: Includes Streamlit app (app.py), trained model files (.pkl), and EDA notebook.

🧰 Built With

Streamlit

Scikit-learn

XGBoost

Pandas

NumPy

👩‍💻 Author

Saijaya Rami Reddy Chilekampalli




