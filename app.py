
import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

from pathlib import Path
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Cybersecurity Threat Detection",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI Cybersecurity Threat Detection System")

st.write(
    "AI-powered Security Log Analysis, "
    "Anomaly Detection and Threat Investigation"
)

st.caption(
    "Educational cybersecurity monitoring prototype "
    "using machine learning."
)

st.divider()

# ==========================================
# 2. LOAD IMPROVED ML MODEL
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = (
    BASE_DIR / "models" / "improved_threat_model.pkl"
)

@st.cache_resource
def load_model(path):
    return joblib.load(path)

if not MODEL_PATH.exists():
    st.error(
        "Improved model not found. "
        "Run python train_improved_model.py first."
    )
    st.stop()

try:
    model = load_model(str(MODEL_PATH))
except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.stop()

# ==========================================
# 3. SIDEBAR AND FILE UPLOAD
# ==========================================

st.sidebar.title("⚙️ Dashboard Controls")

uploaded_file = st.file_uploader(
    "Upload Cybersecurity Log File",
    type=["csv"]
)

if uploaded_file is None:
    st.info("Upload a CSV file to start analysis.")

    st.write("### Required CSV Columns")

    st.code(
        "failed_attempts,bytes_sent,hour\n"
        "0,500,10\n"
        "15,1000,11\n"
        "25,120000,2",
        language="csv"
    )

    st.stop()

# ==========================================
# 4. READ CSV
# ==========================================

try:
    df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"CSV reading error: {e}")
    st.stop()

if df.empty:
    st.error("The uploaded CSV is empty.")
    st.stop()

st.subheader("📂 Uploaded Security Logs")

st.dataframe(
    df,
    use_container_width=True
)

# ==========================================
# 5. DATA VALIDATION
# ==========================================

features = [
    "failed_attempts",
    "bytes_sent",
    "hour"
]

if "hour" not in df.columns and "timestamp" in df.columns:
    df["hour"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    ).dt.hour

missing = [
    col for col in features
    if col not in df.columns
]

if missing:
    st.error(f"Missing required columns: {missing}")
    st.stop()

X = df[features].copy()

for col in features:
    X[col] = pd.to_numeric(
        X[col],
        errors="coerce"
    )

if X.isnull().any().any():
    st.error(
        "Missing or invalid numerical values "
        "were found in the dataset."
    )
    st.stop()

if (
    (X["failed_attempts"] < 0).any()
    or (X["bytes_sent"] < 0).any()
    or ((X["hour"] < 0) | (X["hour"] > 23)).any()
):
    st.error("Invalid security log values detected.")
    st.stop()

df[features] = X

# ==========================================
# 6. AI ANOMALY DETECTION
# ==========================================

try:
    predictions = model.predict(X)

    anomaly_scores = -model.decision_function(X)

except Exception as e:
    st.error(f"Prediction failed: {e}")
    st.stop()

df["Predicted_Label"] = (
    predictions == -1
).astype(int)

df["Threat_Status"] = df["Predicted_Label"].map({
    0: "Normal",
    1: "Suspicious"
})

df["Anomaly_Score"] = anomaly_scores

# ==========================================
# 7. ATTACK EXPLANATIONS
# ==========================================

def explain_threat(row):

    if row["Threat_Status"] == "Normal":
        return "No anomaly flagged"

    failed = row["failed_attempts"]
    traffic = row["bytes_sent"]

    if failed >= 10 and traffic >= 50000:
        return "Multiple Suspicious Indicators"

    elif failed >= 10:
        return "Possible Brute Force Activity"

    elif traffic >= 50000:
        return "Unusual Network Traffic"

    return "Unclassified Anomaly"


df["Threat_Explanation"] = df.apply(
    explain_threat,
    axis=1
)

# ==========================================
# 8. THREAT SEVERITY
# ==========================================

def classify_severity(row):

    if row["Threat_Status"] == "Normal":
        return "Low"

    if (
        row["failed_attempts"] >= 20
        or row["bytes_sent"] >= 100000
    ):
        return "High"

    return "Medium"


df["Severity"] = df.apply(
    classify_severity,
    axis=1
)

# ==========================================
# 9. DASHBOARD METRICS
# ==========================================

total = len(df)

suspicious = int(
    (df["Threat_Status"] == "Suspicious").sum()
)

normal = total - suspicious

high = int(
    (df["Severity"] == "High").sum()
)

medium = int(
    (df["Severity"] == "Medium").sum()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("📊 Total Logs", total)
col2.metric("✅ Normal Logs", normal)
col3.metric("🚨 Suspicious Logs", suspicious)
col4.metric("🔴 High Severity", high)

st.divider()

# ==========================================
# 10. SECURITY ALERTS
# ==========================================

st.subheader("🚨 Security Alerts")

if suspicious > 0:
    st.warning(
        f"{suspicious} unusual security records detected."
    )
else:
    st.success("No anomalies detected.")

if high > 0:
    st.error(
        f"{high} high-priority records "
        "require investigation."
    )

if medium > 0:
    st.info(
        f"{medium} medium-priority records "
        "were identified."
    )

# ==========================================
# 11. INTERACTIVE FILTERS
# ==========================================

st.sidebar.subheader("🔍 Log Filters")

severity_filter = st.sidebar.selectbox(
    "Severity",
    ["All", "High", "Medium", "Low"]
)

status_filter = st.sidebar.selectbox(
    "Threat Status",
    ["All", "Normal", "Suspicious"]
)

filtered_df = df.copy()

if severity_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Severity"] == severity_filter
    ]

if status_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Threat_Status"] == status_filter
    ]

st.subheader("🔍 Filtered Security Logs")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ==========================================
# 12. SECURITY ANALYTICS
# ==========================================

st.subheader("📈 Security Analytics")

chart1, chart2 = st.columns(2)

with chart1:

    status_counts = (
        df["Threat_Status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = ["Status", "Count"]

    fig1 = px.pie(
        status_counts,
        names="Status",
        values="Count",
        title="Normal vs Suspicious Logs",
        color="Status",
        color_discrete_map={
            "Normal": "green",
            "Suspicious": "red"
        }
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with chart2:

    severity_counts = (
        df["Severity"]
        .value_counts()
        .reset_index()
    )

    severity_counts.columns = ["Severity", "Count"]

    fig2 = px.bar(
        severity_counts,
        x="Severity",
        y="Count",
        color="Severity",
        title="Threat Severity Distribution",
        color_discrete_map={
            "High": "red",
            "Medium": "orange",
            "Low": "green"
        }
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ==========================================
# 13. SUSPICIOUS ACTIVITY DETAILS
# ==========================================

st.subheader("⚠️ Suspicious Activities")

threats = df[
    df["Threat_Status"] == "Suspicious"
].copy()

if not threats.empty:

    st.dataframe(
        threats,
        use_container_width=True
    )

    attack_counts = (
        threats["Threat_Explanation"]
        .value_counts()
        .reset_index()
    )

    attack_counts.columns = [
        "Explanation",
        "Count"
    ]

    fig3 = px.bar(
        attack_counts,
        x="Explanation",
        y="Count",
        color="Explanation",
        title="Suspicious Activity Categories"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

else:
    st.info("No suspicious records found.")

# ==========================================
# 14. TOP SUSPICIOUS IP ADDRESSES
# ==========================================

st.subheader("🌐 Suspicious IP Address Analysis")

if "source_ip" in df.columns:

    if not threats.empty:

        ip_counts = (
            threats["source_ip"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        ip_counts.columns = [
            "Source IP",
            "Suspicious Events"
        ]

        st.dataframe(
            ip_counts,
            use_container_width=True
        )

        fig_ip = px.bar(
            ip_counts,
            x="Source IP",
            y="Suspicious Events",
            title="Top 10 Flagged IP Addresses"
        )

        st.plotly_chart(
            fig_ip,
            use_container_width=True
        )

    else:
        st.info("No flagged IP addresses.")

else:
    st.info(
        "Upload a dataset containing source_ip "
        "to view IP address analysis."
    )

# ==========================================
# 15. HOURLY THREAT ANALYSIS
# ==========================================

st.subheader("🕒 Hourly Security Activity")

hourly_counts = (
    df.groupby(["hour", "Threat_Status"])
    .size()
    .reset_index(name="Count")
)

fig_hour = px.line(
    hourly_counts,
    x="hour",
    y="Count",
    color="Threat_Status",
    markers=True,
    title="Security Events by Hour"
)

fig_hour.update_layout(
    xaxis_title="Hour of Day",
    yaxis_title="Number of Events"
)

st.plotly_chart(
    fig_hour,
    use_container_width=True
)

# ==========================================
# 16. CONFUSION MATRIX & MODEL EVALUATION
# ==========================================

st.subheader("🧠 Machine Learning Evaluation")

if "actual_label" in df.columns:

    y_true = pd.to_numeric(
        df["actual_label"],
        errors="coerce"
    )

    if (
        y_true.isnull().any()
        or not y_true.isin([0, 1]).all()
    ):
        st.warning(
            "actual_label must contain only "
            "0 (normal) and 1 (suspicious)."
        )

    else:

        y_true = y_true.astype(int)
        y_pred = df["Predicted_Label"]

        accuracy = accuracy_score(y_true, y_pred)

        precision = precision_score(
            y_true,
            y_pred,
            zero_division=0
        )

        recall = recall_score(
            y_true,
            y_pred,
            zero_division=0
        )

        f1 = f1_score(
            y_true,
            y_pred,
            zero_division=0
        )

        m1, m2, m3, m4 = st.columns(4)

        m1.metric("Accuracy", f"{accuracy:.2%}")
        m2.metric("Precision", f"{precision:.2%}")
        m3.metric("Recall", f"{recall:.2%}")
        m4.metric("F1 Score", f"{f1:.2%}")

        cm = confusion_matrix(
            y_true,
            y_pred,
            labels=[0, 1]
        )

        fig_cm = px.imshow(
            cm,
            x=[
                "Predicted Normal",
                "Predicted Suspicious"
            ],
            y=[
                "Actual Normal",
                "Actual Suspicious"
            ],
            text_auto=True,
            color_continuous_scale="Blues",
            title="Confusion Matrix"
        )

        fig_cm.update_layout(
            xaxis_title="Predicted Label",
            yaxis_title="Actual Label"
        )

        st.plotly_chart(
            fig_cm,
            use_container_width=True
        )

        st.text(
            classification_report(
                y_true,
                y_pred,
                target_names=[
                    "Normal",
                    "Suspicious"
                ],
                zero_division=0
            )
        )

        st.caption(
            "Evaluation results apply to the "
            "uploaded labeled dataset only."
        )

else:
    st.info(
        "Upload a CSV with an actual_label column "
        "to display model evaluation metrics."
    )

# ==========================================
# 17. DOWNLOAD REPORT
# ==========================================

st.subheader("📥 Download Security Report")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Security Analysis Report",
    data=csv_data,
    file_name="cybersecurity_analysis_report.csv",
    mime="text/csv"
)

st.caption(
    "This application is an educational prototype. "
    "AI anomalies are not confirmed cyberattacks. "
    "Threat explanations and severity use "
    "demonstration rules."
)
