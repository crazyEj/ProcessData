import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
if current_directory not in sys.path:
    sys.path.insert(0, current_directory)

if "core_engine" in sys.modules:
    del sys.modules["core_engine"]

from core_engine import DataTriageEngine

# App Configuration
st.set_page_config(page_title="Data Triage Studio", layout="wide", page_icon="🛠️")
st.title("🛠️ Data Triage & Cleaning Studio")
st.caption("Click the '⚙️ Features' button in the sidebar to view available workspaces.")

# Initialize Persistent Sessions
if "working_df" not in st.session_state:
    st.session_state.working_df = None
if "audit_trail" not in st.session_state:
    st.session_state.audit_trail = []
if "show_features" not in st.session_state:
    st.session_state.show_features = False
if "current_feature" not in st.session_state:
    st.session_state.current_feature = "📊 Structural Profiling"
if "feature_status" not in st.session_state:
    st.session_state.feature_status = {}

def log_action(action: str):
    st.session_state.audit_trail.append(action)

# =========================================================
# 📁 SIDEBAR CONTROLLER DECK
# =========================================================
st.sidebar.header("📁 Control Center")

# 1. File Upload Component
uploaded_file = st.sidebar.file_uploader("Upload Raw/Damaged Dataset", type=["csv"])

if uploaded_file:
    if st.session_state.working_df is None:
        try:
            imported_df = DataTriageEngine.robust_csv_import(uploaded_file)
            st.session_state.working_df = imported_df
            st.session_state.feature_status = DataTriageEngine.evaluate_available_features(imported_df)
            log_action(f"Initialization: Loaded raw data with {len(imported_df)} records.")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Critical Parsing Error: {e}")

st.sidebar.markdown("---")

# 2. THE FEATURE TOGGLE BUTTON
if st.sidebar.button("⚙️ Features", use_container_width=True):
    st.session_state.show_features = not st.session_state.show_features

# Master list of features
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

# 3. RENDER DYNAMIC BUTTONS
if st.session_state.show_features:
    st.sidebar.write("### Available Workspaces")
    
    if st.session_state.working_df is not None:
        status = st.session_state.feature_status
        
        for f in all_features:
            is_enabled = status.get(f["id"], False)
            if f["id"] == "forecast" and not is_enabled:
                continue
            if f["id"] == "ml_studio" and not is_enabled:
                continue
                
            if st.sidebar.button(f["label"], key=f"btn_{f['id']}", use_container_width=True):
                st.session_state.current_feature = f["label"]
    else:
        st.sidebar.caption("Please upload a CSV file to unlock feature buttons.")

# Global Export Controller
if st.session_state.working_df is not None:
    st.sidebar.markdown("---")
    st.sidebar.subheader("💾 Production Export")
    export_bytes = st.session_state.working_df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="Download Clean CSV Output",
        data=export_bytes,
        file_name="triage_studio_export.csv",
        mime="text/csv"
    )

# =========================================================
# 🖥️ MAIN APPLICATION INTERFACE
# =========================================================
if st.session_state.working_df is not None:
    current_df = st.session_state.working_df
    feature_choice = st.session_state.current_feature

    # Upper Dashboard Layout
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("### Data Canvas Preview")
        st.dataframe(current_df.head(5), use_container_width=True)
    with col2:
        st.write("### Workflow History")
        if st.session_state.audit_trail:
            for item in st.session_state.audit_trail[-3:]:
                st.caption(f"• {item}")
        if st.button("Reset Project Pipeline"):
            st.session_state.working_df = None
            st.session_state.audit_trail = []
            st.session_state.feature_status = {}
            st.session_state.current_feature = "📊 Structural Profiling"
            st.rerun()

    st.markdown("---")
    st.write(f"### Active Workspace: {feature_choice}")

    # ROUTING SYSTEM
    
    # 1. Structural Profiling
    if "📊" in feature_choice:
        health_metrics = DataTriageEngine.get_health_metrics(current_df)
        st.dataframe(health_metrics, use_container_width=True)

    # 2. Auto-Imputation Engine
    elif "🧼" in feature_choice:
        st.info("System rule: Fills missing numbers with Column Medians, and categorical blanks with Column Modes/Unknown markers.")
        if st.button("Execute Global Auto-Imputation Routine"):
            st.session_state.working_df = DataTriageEngine.auto_impute(current_df)
            log_action("Auto-Imputation Run: Erased null fields dynamically.")
            st.success("Dataset repaired!")
            st.rerun()

    # 3. Text Inconsistency Fix
    elif "📝" in feature_choice:
        text_cols = current_df.select_dtypes(include=['object', 'category']).columns.tolist()
        if text_cols:
            select_col = st.selectbox("Target String Field", text_cols)
            base_word = st.text_input("Intended Standard Spelling", placeholder="Type exact string...")
            match_score = st.slider("Strictness Boundary (Fuzzy Weight)", 0, 100, 75)
            if base_word and st.button("Execute String Correction"):
                repaired_df, fixes = DataTriageEngine.fuzzy_standardize(current_df, select_col, base_word, match_score)
                st.session_state.working_df = repaired_df
                log_action(f"Fuzzy Grouping Applied: Aligned deviations in '{select_col}' to '{base_word}'.")
                st.success(f"Adjusted variations: {fixes}")
                st.rerun()

    # 4. ML Anomaly Isolation
    elif "🚨" in feature_choice:
        num_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            selected_features = st.multiselect("Select Evaluation Space Vectors", num_cols, default=num_cols)
            contamination_rate = st.slider("Contamination Bound", 0.01, 0.25, 0.05)
            if selected_features and st.button("Deploy Anomaly Scanner Models"):
                flagged_df, total_anomalies = DataTriageEngine.isolate_anomalies(current_df, selected_features, contamination_rate)
                st.write(f"Flagged Points Detected: **{total_anomalies}** abnormal rows identified.")
                st.dataframe(flagged_df.sort_values(by="Anomaly_Flag", ascending=True), use_container_width=True)

    # 5. Smart Sorting & Deep Search
    elif "🔍" in feature_choice:
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            query_str = st.text_input("Search terms across any dimension", placeholder="Enter key terms...")
            regex_toggle = st.checkbox("Toggle Expression Matching (Regex Engine)")
            filtered_df = DataTriageEngine.global_deep_search(current_df, query_str, use_regex=regex_toggle)
        with col_s2:
            sort_target = st.selectbox("Key Sorting Vector", current_df.columns)
            direction = st.radio("Direction Rules", ["Ascending", "Descending"])
            is_asc = True if "Ascending" in direction else False
            try:
                filtered_df = filtered_df.sort_values(by=sort_target, ascending=is_asc, na_position='last')
            except:
                filtered_df = filtered_df.assign(tmp=filtered_df[sort_target].astype(str)).sort_values(by="tmp", ascending=is_asc).drop(columns=["tmp"])
        st.dataframe(filtered_df, use_container_width=True)

    # 6. RE-ENGINEERED: HIGH-ANALYTIC TREND FORECASTING
    elif "📈" in feature_choice:
        st.write("### Advanced Time-Series Analytics & Value Forecasting")
        st.caption("Aggregate historical records into moving price benchmarks and model future trajectories.")
        
        all_cols = current_df.columns.tolist()
        num_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()
        
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            col_date = st.selectbox("Select Timeline/Date Axis Column", all_cols)
        with col_f2:
            col_val = st.selectbox("Select Target Variable to Forecast (e.g., Price/Value)", num_cols)
        with col_f3:
            time_freq = st.selectbox("Aggregation Time Window Step (Frequency)", 
                                     options=[("Daily", "D"), ("Weekly", "W"), ("Monthly", "M")], 
                                     format_func=lambda x: x[0])
            
        horizon = st.slider(f"Prediction Horizon Steps ({time_freq[0]} steps into the future)", 1, 24, 6)
        
        if st.button("Generate Analytical Forecasting Analytics", use_container_width=True):
            try:
                with st.spinner("Resampling valuations and compiling exponential trend lines..."):
                    forecast_data = DataTriageEngine.generate_forecast(
                        current_df, col_date, col_val, periods=horizon, freq=time_freq[1]
                    )
                    
                    log_action(f"Trend Analysis Run: Forecasted '{col_val}' forward by {horizon} steps.")
                    
                    st.markdown("---")
                    st.write(f"#### 📊 Interactive Time-Series Projection Dashboard: {col_val}")
                    
                    # Graph Section
                    st.line_chart(data=forecast_data, x="Timeline Axis", y=["Historical Value", "Predicted Value"])
                    
                    # Analytic Summaries Cards
                    st.write("#### 📈 Key Forecast Performance Indicators")
                    c_card1, c_card2, c_card3 = st.columns(3)
                    
                    clean_history = forecast_data["Historical Value"].dropna()
                    clean_predictions = forecast_data["Predicted Value"].dropna()
                    
                    base_avg = clean_history.mean()
                    terminal_val = clean_predictions.iloc[-1]
                    pct_delta = ((terminal_val - clean_history.iloc[-1]) / clean_history.iloc[-1]) * 100
                    
                    with c_card1:
                        st.metric(label="Historical Base Baseline (Average)", value=f"₱ {base_avg:,.2f}")
                    with c_card2:
                        st.metric(label="Target Terminal End Valuation", value=f"₱ {terminal_val:,.2f}")
                    with c_card3:
                        st.metric(label="Expected Price Velocity Deviation", value=f"{pct_delta:+.2f}%")
                        
                    # Detailed Tabular Layout Ledger
                    st.write("#### 📝 Consolidated History & Prediction Ledger")
                    st.dataframe(forecast_data, use_container_width=True)
                    
            except Exception as e:
                st.error(f"Trend Engine Pipeline Interrupted: Validate that your chosen time column contains structural date properties. Error context: {e}")

    # 7. Pivot Analyzer
    elif "🗂️" in feature_choice:
        all_cols = current_df.columns.tolist()
        num_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()
        pivot_row = st.selectbox("Group By (Rows)", all_cols)
        pivot_val = st.selectbox("Target Calculation Field (Values)", num_cols)
        math_operation = st.selectbox("Aggregation Math Metric", ["sum", "mean", "count", "max", "min"])
        if st.button("Generate Pivot Aggregations"):
            pivot_table = DataTriageEngine.build_pivot_table(current_df, pivot_row, pivot_val, math_operation)
            st.dataframe(pivot_table, use_container_width=True)

    # 8. Client Consolidation Merger
    elif "🤝" in feature_choice:
        all_columns = current_df.columns.tolist()
        numeric_columns = current_df.select_dtypes(include=[np.number]).columns.tolist()
        merge_target = st.selectbox("Select column with repeating names/clients", all_columns)
        value_target = st.selectbox("Select numeric column to combine", numeric_columns)
        math_strategy = st.selectbox("How should we merge their numeric values?", ["sum", "mean", "max", "count"])
        if st.button("Run Consolidation & Flatten Dataset"):
            st.session_state.working_df = DataTriageEngine.aggregate_and_collapse(current_df, merge_target, value_target, math_strategy)
            st.success("Dataset successfully flattened!")
            st.rerun()

    # 9. Predictive ML Studio Workspace
    elif "🧠" in feature_choice:
        st.write("### Automated Machine Learning Studio Pipeline")
        all_cols = current_df.columns.tolist()
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            target_var = st.selectbox("Select Target Label", all_cols, index=len(all_cols)-1)
        with col_m2:
            default_features = [c for c in all_cols if c != target_var]
            selected_features = st.multiselect("Select Feature Dimensions", all_cols, default=default_features)

        if len(selected_features) > 0 and st.button("Train Automated Machine Learning Model", use_container_width=True):
            try:
                results = DataTriageEngine.run_machine_learning_pipeline(current_df, target_var, selected_features)
                st.markdown("---")
                st.write(f"### 🎉 Pipeline Execution Results: {results['task_type']} Engine")
                c1, c2 = st.columns(2)
                with c1: st.metric(label=results["score_metric"], value=f"{results['score_value']}")
                with c2: st.metric(label="Evaluation Strategy", value="Cross-Validation Splitting") if results["error_value"] is None else st.metric(label="Mean Absolute Error (MAE)", value=f"{results['error_value']}")
                ch1, ch2 = st.columns([1, 1])
                with ch1:
                    st.write("#### 📊 Feature Importance Ranking")
                    st.bar_chart(data=results["feature_importance"], x="Feature Vector", y="Significance Weight")
                with ch2:
                    st.write("#### 🎯 Prediction Sample Preview")
                    st.dataframe(results["preview_df"].head(10), use_container_width=True)
            except Exception as e:
                st.error(f"Pipeline Crashed: {e}")
else:
    st.info("System standing by. Please upload a broken or unfixed file in the sidebar controller to begin.")