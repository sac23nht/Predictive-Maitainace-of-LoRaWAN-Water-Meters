import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os

# ================================
# 🔹 Model Paths
# ================================
# Resolved relative to this file so the app runs unmodified on any machine
# or hosting platform (Streamlit Community Cloud, Docker, Render, etc.).
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATHS = {
    "Logistic Regression": os.path.join(BASE_DIR, "logistic_regression_pipeline.pkl"),
    "Random Forest": os.path.join(BASE_DIR, "random_forest_best_pipeline.pkl"),
    "XGBoost": os.path.join(BASE_DIR, "xgboost_best_pipeline.pkl"),
}

# ================================
# 🔹 Check for Missing Models
# ================================
missing_files = [path for path in MODEL_PATHS.values() if not os.path.exists(path)]
if missing_files:
    st.error("❌ Missing model files:\n" + "\n".join(missing_files))
    st.stop()

# Load models
models = {name: joblib.load(path) for name, path in MODEL_PATHS.items()}

# ================================
# 🔹 Streamlit UI Setup
# ================================
st.set_page_config(page_title="Meter Risk Prediction", layout="centered")
st.title("🔍 Meter Risk Prediction App")

# Model selection
selected_model_name = st.selectbox("Select Model", list(models.keys()))
model = models[selected_model_name]

# Prediction mode selection
st.subheader("Select Prediction Mode")
mode = st.radio(
    "Choose how the model should predict:",
    ["Default", "Recall-Focused", "Precision-Focused"],
    horizontal=True
)

# Set default thresholds
if mode == "Default":
    threshold = 0.5
    st.info("✅ Default mode selected (Fixed threshold = 0.5)")
else:
    default_threshold = 0.3 if mode == "Recall-Focused" else 0.7
    st.write(f"⚙️ {mode} Mode: Adjust decision threshold")
    threshold = st.slider(
        "Select Decision Threshold",
        min_value=0.1,
        max_value=0.9,
        value=default_threshold,
        step=0.01,
        help="Lower threshold increases recall; higher increases precision"
    )

# ================================
# 🔹 Define Feature Inputs
# ================================
FEATURES_INFO = {
    "RSSI_dBm": {"min": -132.0, "max": -80.0, "step": 1.0, "default": -100.0},
    "DistanceToNearestGateway (meters)": {"min": 50.0, "max": 1000.0, "step": 1.0, "default": 200.0},
    "SNR_dB": {"min": -21.0, "max": 19.0, "step": 0.1, "default": 0.0},
    "Depth_mm": {"min": 100.0, "max": 800.0, "step": 1.0, "default": 300.0},
    "SpreadingFactor": {"min": 7.0, "max": 12.0, "step": 1.0, "default": 7.0}
}

st.subheader("📥 Enter Feature Values")

# Collect numeric inputs
user_input = {}
for feature, info in FEATURES_INFO.items():
    user_input[feature] = st.slider(
        label=feature,
        min_value=info["min"],
        max_value=info["max"],
        value=info["default"],
        step=info["step"]
    )

# Lid type dropdown
lidtype = st.selectbox("Select Lid Type", ["Plastic", "Composite", "Cast Iron"])
user_input["LidType_Composite"] = 1 if lidtype == "Composite" else 0
user_input["LidType_Plastic"] = 1 if lidtype == "Plastic" else 0
# Cast Iron = (0,0)

# Convert to DataFrame
input_df = pd.DataFrame([user_input])

# ================================
# 🔹 Align Columns with Training
# ================================
classifier_step_name = None
for name, step in model.named_steps.items():
    if hasattr(step, "feature_names_in_"):
        classifier_step_name = name
        break

if classifier_step_name is None:
    st.error("⚠️ Could not determine classifier feature names from pipeline.")
    st.stop()

expected_features = model.named_steps[classifier_step_name].feature_names_in_
input_df = input_df[expected_features]

# ================================
# 🔹 Prediction
# ================================
if st.button("Predict"):
    try:
        # Get prediction probability
        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(input_df)[0][1]
        else:
            prob = float(model.predict(input_df)[0])

        # Apply threshold
        prediction = 1 if prob >= threshold else 0

        # Display results
        st.subheader("🧠 Prediction Result")

        if prediction == 1:
            st.error(f"⚠️ The meter is predicted to be **AT RISK**.\n\nRisk Probability: **{prob:.2f}**")
        else:
            st.success(f"✅ The meter is predicted to be **SAFE**.\n\nRisk Probability: **{prob:.2f}**")

        # Show mode details
        st.info(
            f"**Mode:** {mode} | **Decision Threshold:** {threshold:.2f}\n\n"
            f"- Recall-Focused → catches more at-risk meters (more false alarms)\n"
            f"- Precision-Focused → fewer false alarms but might miss some risks"
        )

    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit, scikit-learn & XGBoost.")
