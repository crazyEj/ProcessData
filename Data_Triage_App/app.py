import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
if current_directory not in sys.path:
    sys.path.insert(0, current_directory)

# Hot reload tracking vectors
for module in ["core_engine", "ui_components"]:
    if module in sys.modules:
        del sys.modules[module]

from core_engine import DataTriageEngine
from ui_components import UIComponents

st.set_page_config(page_title="Data Triage Studio", layout="wide", page_icon="🛠️")
st.title("🛠️ Data Triage & Cleaning Studio")
st.caption("Click the '⚙️ Features' button in the sidebar to view available workspaces.")

if "working_df" not in st.session_state: st.session_state.working_df = None
if "audit_trail" not in st.session_state: st.session_state.audit_trail = []
if "show_features" not in st.session_state: st.session_state.show_features = False
if "current_feature" not in st.session_state: st.session_state.current_feature = "📊 Structural Profiling"
if "feature_status" not in st.session_state: st.session_state.feature_status = {}
if "trained_ml_data" not in st.session_state: st.session_state.trained_ml_data = None

def log_action(action: str): st.session_state.audit_trail.append(action)

# --- CONTROL SIDEBAR ---
st.sidebar.header("📁 Control Center")
uploaded_file = st.sidebar.file_uploader("Upload Raw/Damaged Dataset", type=["csv"])

if uploaded_file and st.session_state.working_df is None:
    try:
        imported_df = DataTriageEngine.robust_csv_import(uploaded_file)
        st.session_state.working_df = imported_df
        st.session_state.feature_status = DataTriageEngine.evaluate_available_features(imported_df)
        log_action(f"Initialization: Loaded raw data with {len(imported_df)} records.")
        st.rerun()
    except Exception as e: st.sidebar.error(f"Critical Parsing Error: {e}")

st.sidebar.markdown("---")
if st.sidebar.button("⚙️ Features", use_container_width=True):
    st.session_state.show_features = not st.session_state.show_features

all_features = [
    {"id": "profile", "label": "📊 Structural Profiling"},
    {"id": "search", "label": "🔍 Smart Sorting & Deep Search"},
    {"id": "impute", "label": "🧼 Auto-Imputation Engine"},
    {"id": "text", "label": "📝 Text Inconsistency Fix"},
    {"id": "anomaly", "label": "🚨 ML Anomaly Isolation"},
    {"id": "pivot", "label": "🗂️ Pivot Analyzer"},
    {"id": "merge", "label": "🤝 Client Consolidation Merger"},
    {"id": "forecast", "label": "📈 Trend Forecasting"},
    {"id": "ml_studio", "label": "🧠 Predictive ML Studio"}
]

if st.session_state.show_features:
    st.sidebar.write("### Available Workspaces")
    if st.session_state.working_df is not None:
        status = st.session_state.feature_status
        for f in all_features:
            if f["id"] in ["forecast", "ml_studio"] and not status.get(f["id"], False): continue
            if st.sidebar.button(f["label"], key=f"btn_{f['id']}", use_container_width=True):
                st.session_state.current_feature = f["label"]

if st.session_state.working_df is not None:
    st.sidebar.markdown("---")
    export_bytes = st.session_state.working_df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(label="Download Clean CSV Output", data=export_bytes, file_name="triage_studio_export.csv", mime="text/csv")

# --- MAIN ENGINE RUNTIME ---
if st.session_state.working_df is not None:
    current_df = st.session_state.working_df
    feature_choice = st.session_state.current_feature

    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("### Data Canvas Preview")
        st.dataframe(current_df.head(5), use_container_width=True)
    with col2:
        st.write("### Workflow History")
        if st.session_state.audit_trail:
            for item in st.session_state.audit_trail[-3:]: st.caption(f"• {item}")
        if st.button("Reset Project Pipeline"):
            st.session_state.working_df, st.session_state.audit_trail, st.session_state.trained_ml_data = None, [], None
            st.session_state.current_feature = "📊 Structural Profiling"
            st.rerun()

    st.markdown("---")
    st.write(f"### Active Workspace: {feature_choice}")

    # ROUTING SYSTEM
    if "📊" in feature_choice:
        st.dataframe(DataTriageEngine.get_health_metrics(current_df), use_container_width=True)

    elif "🧼" in feature_choice:
        if st.button("Execute Global Auto-Imputation Routine"):
            st.session_state.working_df = DataTriageEngine.auto_impute(current_df)
            log_action("Auto-Imputation Run: Erased null fields dynamically.")
            st.success("Dataset repaired!"), st.rerun()

    elif "📝" in feature_choice:
        text_cols = current_df.select_dtypes(include=['object', 'category']).columns.tolist()
        if text_cols:
            select_col = st.selectbox("Target String Field", text_cols)
            base_word = st.text_input("Intended Standard Spelling")
            match_score = st.slider("Strictness Boundary", 0, 100, 75)
            if base_word and st.button("Execute String Correction"):
                repaired_df, fixes = DataTriageEngine.fuzzy_standardize(current_df, select_col, base_word, match_score)
                st.session_state.working_df = repaired_df
                log_action(f"Fuzzy Grouping Applied: Aligned deviations in '{select_col}'.")
                st.success(f"Adjusted: {fixes}"), st.rerun()

    elif "🚨" in feature_choice:
        num_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            selected_features = st.multiselect("Select Evaluation Vectors", num_cols, default=num_cols)
            contamination_rate = st.slider("Contamination Bound", 0.01, 0.25, 0.05)
            if selected_features and st.button("Deploy Anomaly Scanner Models"):
                flagged_df, total_anomalies = DataTriageEngine.isolate_anomalies(current_df, selected_features, contamination_rate)
                st.write(f"Flagged Points: **{total_anomalies}** abnormal rows.")
                st.dataframe(flagged_df.sort_values(by="Anomaly_Flag", ascending=True), use_container_width=True)

    elif "🔍" in feature_choice:
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            query_str = st.text_input("Search terms")
            regex_toggle = st.checkbox("Toggle Regex Engine")
            filtered_df = DataTriageEngine.global_deep_search(current_df, query_str, use_regex=regex_toggle)
        with col_s2:
            sort_target = st.selectbox("Key Sorting Vector", current_df.columns)
            is_asc = True if "Ascending" in st.radio("Direction", ["Ascending", "Descending"]) else False
            try: filtered_df = filtered_df.sort_values(by=sort_target, ascending=is_asc)
            except: filtered_df = filtered_df.assign(tmp=filtered_df[sort_target].astype(str)).sort_values(by="tmp", ascending=is_asc).drop(columns=["tmp"])
        st.dataframe(filtered_df, use_container_width=True)

    elif "📈" in feature_choice:
        all_cols = current_df.columns.tolist()
        num_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1: col_date = st.selectbox("Select Timeline Axis Column", all_cols)
        with col_f2: col_val = st.selectbox("Select Target Variable to Forecast", num_cols)
        with col_f3: time_freq = st.selectbox("Frequency Window", options=[("Daily", "D"), ("Weekly", "W"), ("Monthly", "M")], format_func=lambda x: x[0])
        horizon = st.slider("Prediction Horizon Steps", 1, 24, 6)
        
        if st.button("Generate Analytical Forecasting Analytics", use_container_width=True):
            try:
                forecast_data = DataTriageEngine.generate_forecast(current_df, col_date, col_val, periods=horizon, freq=time_freq[1])
                log_action(f"ARIMA Forecast Run on '{col_val}' for {horizon} intervals.")
                UIComponents.render_forecast_dashboard(forecast_data, col_val)
            except Exception as e: st.error(f"Time-Series Pipeline Failure: {e}")

    elif "🗂️" in feature_choice:
        all_cols = current_df.columns.tolist()
        num_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()
        pivot_row = st.selectbox("Group By (Rows)", all_cols)
        pivot_val = st.selectbox("Target Calculation Field", num_cols)
        math_operation = st.selectbox("Aggregation Metric", ["sum", "mean", "count", "max", "min"])
        if st.button("Generate Pivot Aggregations"):
            st.dataframe(DataTriageEngine.build_pivot_table(current_df, pivot_row, pivot_val, math_operation), use_container_width=True)

    elif "🤝" in feature_choice:
        all_columns = current_df.columns.tolist()
        numeric_columns = current_df.select_dtypes(include=[np.number]).columns.tolist()
        merge_target = st.selectbox("Select column with repeating labels", all_columns)
        value_target = st.selectbox("Select numeric column to combine", numeric_columns)
        math_strategy = st.selectbox("Strategy", ["sum", "mean", "max", "count"])
        if st.button("Run Consolidation"):
            st.session_state.working_df = DataTriageEngine.aggregate_and_collapse(current_df, merge_target, value_target, math_strategy)
            st.success("Dataset successfully flattened!"), st.rerun()
    elif "🧠" in feature_choice:
        st.write("### Automated Machine Learning Studio Pipeline & What-If Canvas")
        all_cols = current_df.columns.tolist()
        col_m1, col_m2 = st.columns(2)
        with col_m1: 
            target_var = st.selectbox("Select Target Label", all_cols, index=len(all_cols)-1)
        with col_m2: 
            selected_features = st.multiselect("Select Feature Dimensions", all_cols, default=[c for c in all_cols if c != target_var])

        if len(selected_features) > 0 and st.button("Train Automated Machine Learning Model", use_container_width=True):
            try:
                with st.spinner("Processing forest pipelines..."):
                    st.session_state.trained_ml_data = DataTriageEngine.run_machine_learning_pipeline(current_df, target_var, selected_features)
                    log_action(f"ML Studio Model Trained on '{target_var}'.")
            except Exception as e: 
                st.error(f"Training Interrupted: {e}")

        if st.session_state.trained_ml_data is not None:
            res = st.session_state.trained_ml_data
            st.markdown("---")
            st.write(f"### 🎉 Pipeline Execution Results: {res['task_type']} Engine")
            c1, c2 = st.columns(2)
            with c1: 
                st.metric(label=res["score_metric"], value=f"{res['score_value']}")
            with c2: 
                if res["error_value"] is None:
                    st.metric(label="Evaluation Strategy", value="Cross-Validation Splitting")
                else:
                    st.metric(label="Mean Absolute Error (MAE)", value=f"{res['error_value']}")
            
            # Render our performance analytics tracking line graph
            UIComponents.render_ml_performance_chart(res["preview_df"])
            
            ch1, ch2 = st.columns([1, 1])
            with ch1: 
                st.write("#### 📊 Feature Importance Ranking")
                st.bar_chart(data=res["feature_importance"], x="Feature Vector", y="Significance Weight")
            with ch2: 
                st.write("#### 🎯 Prediction Sample Preview")
                st.dataframe(res["preview_df"].head(5), use_container_width=True)
                
            # Render our modular simulation dashboard element
            UIComponents.render_what_if_canvas(current_df, res)
else:
    st.info("System standing by. Please upload a broken or unfixed file in the sidebar controller to begin.")
  