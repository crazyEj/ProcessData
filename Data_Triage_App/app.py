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

# Inject custom CSS immediately
UIComponents.inject_custom_css()

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

# Sidebar upload section with enhanced styling
sidebar_upload_html = """
<div class="custom-card" style="margin-bottom: 16px;">
    <p style="margin: 0 0 8px 0; color: #cbd5e1; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600;">📤 Import Dataset</p>
</div>
"""
st.sidebar.markdown(sidebar_upload_html, unsafe_allow_html=True)

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
if st.sidebar.button("⚙️ Features", use_container_width=True, help="View all available data processing features"):
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
    st.sidebar.markdown("### 🎯 Available Workspaces")
    if st.session_state.working_df is not None:
        status = st.session_state.feature_status
        for f in all_features:
            if f["id"] in ["forecast", "ml_studio"] and not status.get(f["id"], False): continue
            feature_btn_html = f"""
            <style>
            .feature-btn-{f['id']} {{
                display: inline-block;
                width: 100%;
                text-align: left;
            }}
            </style>
            """
            st.sidebar.markdown(feature_btn_html, unsafe_allow_html=True)
            if st.sidebar.button(f["label"], key=f"btn_{f['id']}", use_container_width=True):
                st.session_state.current_feature = f["label"]

if st.session_state.working_df is not None:
    st.sidebar.markdown("---")
    
    # Data stats in sidebar
    stats_html = f"""
    <div class="custom-card">
        <p style="margin: 0 0 8px 0; color: #cbd5e1; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600;">📊 Dataset Stats</p>
        <div style="color: #f1f5f9; font-size: 13px; line-height: 1.8;">
            <div>📈 Rows: <strong>{len(st.session_state.working_df)}</strong></div>
            <div>📋 Columns: <strong>{len(st.session_state.working_df.columns)}</strong></div>
            <div>🚨 Missing: <strong>{st.session_state.working_df.isnull().sum().sum()}</strong></div>
        </div>
    </div>
    """
    st.sidebar.markdown(stats_html, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    export_bytes = st.session_state.working_df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="📥 Download Clean CSV",
        data=export_bytes,
        file_name="triage_studio_export.csv",
        mime="text/csv",
        use_container_width=True
    )

# --- MAIN ENGINE RUNTIME ---
if st.session_state.working_df is not None:
    current_df = st.session_state.working_df
    feature_choice = st.session_state.current_feature

    col1, col2 = st.columns([3, 1])
    with col1:
        preview_header = """
        <div class="custom-card" style="margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 24px;">📊</span>
                <h3 style="margin: 0; color: #f1f5f9;">Data Canvas Preview</h3>
            </div>
        </div>
        """
        st.markdown(preview_header, unsafe_allow_html=True)
        st.dataframe(current_df.head(5), use_container_width=True)
    with col2:
        history_header = """
        <div class="custom-card" style="margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 24px;">📜</span>
                <h3 style="margin: 0; color: #f1f5f9;">Workflow History</h3>
            </div>
        </div>
        """
        st.markdown(history_header, unsafe_allow_html=True)
        if st.session_state.audit_trail:
            history_items = ""
            for item in st.session_state.audit_trail[-3:]:
                history_items += f"<div style='color: #cbd5e1; font-size: 12px; margin: 6px 0; padding: 6px; background: rgba(99, 102, 241, 0.1); border-radius: 4px;'>• {item}</div>"
            st.markdown(history_items, unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: #cbd5e1; font-size: 12px;'>No actions yet</p>", unsafe_allow_html=True)
            
        if st.button("🔄 Reset Project", use_container_width=True, help="Clear all data and start fresh"):
            st.session_state.working_df, st.session_state.audit_trail, st.session_state.trained_ml_data = None, [], None
            st.session_state.current_feature = "📊 Structural Profiling"
            st.rerun()

    st.markdown("---")
    
    # Feature title with styling
    feature_title_html = f"""
    <div style="
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(236, 72, 153, 0.05) 100%);
        border-left: 4px solid #6366f1;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 20px;
    ">
        <h2 style="margin: 0; color: #f1f5f9;">{feature_choice}</h2>
    </div>
    """
    st.markdown(feature_title_html, unsafe_allow_html=True)

    # ROUTING SYSTEM
    if "📊" in feature_choice:
        profile_header = """
        <div class="custom-card" style="margin-bottom: 16px;">
            <h4 style="margin: 0; color: #f1f5f9;">Dataset Health Profile</h4>
            <p style="margin: 8px 0 0 0; color: #cbd5e1; font-size: 13px;">Comprehensive analysis of data quality, missing values, and type consistency</p>
        </div>
        """
        st.markdown(profile_header, unsafe_allow_html=True)
        st.dataframe(DataTriageEngine.get_health_metrics(current_df), use_container_width=True)

    elif "🧼" in feature_choice:
        impute_header = """
        <div class="custom-card" style="margin-bottom: 16px;">
            <h4 style="margin: 0; color: #f1f5f9;">Auto-Imputation Engine</h4>
            <p style="margin: 8px 0 0 0; color: #cbd5e1; font-size: 13px;">Automatically fill missing values using intelligent algorithms</p>
        </div>
        """
        st.markdown(impute_header, unsafe_allow_html=True)
        if st.button("Execute Global Auto-Imputation Routine", use_container_width=True):
            st.session_state.working_df = DataTriageEngine.auto_impute(current_df)
            log_action("Auto-Imputation Run: Erased null fields dynamically.")
            st.success("✅ Dataset repaired!")
            st.rerun()

    elif "📝" in feature_choice:
        text_header = """
        <div class="custom-card" style="margin-bottom: 16px;">
            <h4 style="margin: 0; color: #f1f5f9;">Text Inconsistency Fix</h4>
            <p style="margin: 8px 0 0 0; color: #cbd5e1; font-size: 13px;">Standardize text entries using fuzzy matching algorithms</p>
        </div>
        """
        st.markdown(text_header, unsafe_allow_html=True)
        text_cols = current_df.select_dtypes(include=['object', 'category']).columns.tolist()
        if text_cols:
            col_t1, col_t2, col_t3 = st.columns(3)
            with col_t1:
                select_col = st.selectbox("Target String Field", text_cols)
            with col_t2:
                base_word = st.text_input("Intended Standard Spelling")
            with col_t3:
                match_score = st.slider("Strictness Boundary", 0, 100, 75)
            
            if base_word and st.button("Execute String Correction", use_container_width=True):
                repaired_df, fixes = DataTriageEngine.fuzzy_standardize(current_df, select_col, base_word, match_score)
                st.session_state.working_df = repaired_df
                log_action(f"Fuzzy Grouping Applied: Aligned deviations in '{select_col}'.")
                st.success(f"✅ Adjusted: {fixes} entries")
                st.rerun()

    elif "🚨" in feature_choice:
        anomaly_header = """
        <div class="custom-card" style="margin-bottom: 16px;">
            <h4 style="margin: 0; color: #f1f5f9;">ML Anomaly Detection</h4>
            <p style="margin: 8px 0 0 0; color: #cbd5e1; font-size: 13px;">Isolate outliers and abnormal data points using Isolation Forest</p>
        </div>
        """
        st.markdown(anomaly_header, unsafe_allow_html=True)
        num_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                selected_features = st.multiselect("Select Evaluation Vectors", num_cols, default=num_cols)
            with col_a2:
                contamination_rate = st.slider("Contamination Bound", 0.01, 0.25, 0.05)
            
            if selected_features and st.button("Deploy Anomaly Scanner Models", use_container_width=True):
                flagged_df, total_anomalies = DataTriageEngine.isolate_anomalies(current_df, selected_features, contamination_rate)
                
                stats_html = f"""
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin: 16px 0;">
                    <div class="metric-card">
                        <p style="margin: 0; color: #cbd5e1; font-size: 11px; text-transform: uppercase;">Flagged Rows</p>
                        <p style="margin: 8px 0 0 0; color: #ef4444; font-size: 24px; font-weight: bold;">{total_anomalies}</p>
                    </div>
                    <div class="metric-card">
                        <p style="margin: 0; color: #cbd5e1; font-size: 11px; text-transform: uppercase;">Clean Rows</p>
                        <p style="margin: 8px 0 0 0; color: #10b981; font-size: 24px; font-weight: bold;">{len(current_df) - total_anomalies}</p>
                    </div>
                    <div class="metric-card">
                        <p style="margin: 0; color: #cbd5e1; font-size: 11px; text-transform: uppercase;">Anomaly Rate</p>
                        <p style="margin: 8px 0 0 0; color: #f59e0b; font-size: 24px; font-weight: bold;">{(total_anomalies/len(current_df)*100):.1f}%</p>
                    </div>
                </div>
                """
                st.markdown(stats_html, unsafe_allow_html=True)
                st.dataframe(flagged_df.sort_values(by="Anomaly_Flag", ascending=True), use_container_width=True)

    elif "🔍" in feature_choice:
        search_header = """
        <div class="custom-card" style="margin-bottom: 16px;">
            <h4 style="margin: 0; color: #f1f5f9;">Smart Sorting & Deep Search</h4>
            <p style="margin: 8px 0 0 0; color: #cbd5e1; font-size: 13px;">Search and filter data with regex support and advanced sorting</p>
        </div>
        """
        st.markdown(search_header, unsafe_allow_html=True)
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            query_str = st.text_input("🔍 Search terms")
            regex_toggle = st.checkbox("🔤 Toggle Regex Engine")
            filtered_df = DataTriageEngine.global_deep_search(current_df, query_str, use_regex=regex_toggle)
        with col_s2:
            sort_target = st.selectbox("📊 Key Sorting Vector", current_df.columns)
            is_asc = True if "Ascending" in st.radio("Direction", ["Ascending", "Descending"]) else False
            try: 
                filtered_df = filtered_df.sort_values(by=sort_target, ascending=is_asc)
            except: 
                filtered_df = filtered_df.assign(tmp=filtered_df[sort_target].astype(str)).sort_values(by="tmp", ascending=is_asc).drop(columns=["tmp"])
        st.dataframe(filtered_df, use_container_width=True)

    elif "📈" in feature_choice:
        forecast_header = """
        <div class="custom-card" style="margin-bottom: 16px;">
            <h4 style="margin: 0; color: #f1f5f9;">Advanced ARIMA Analytics</h4>
            <p style="margin: 8px 0 0 0; color: #cbd5e1; font-size: 13px;">Time-series forecasting with 95% confidence bands and uncertainty quantification</p>
        </div>
        """
        st.markdown(forecast_header, unsafe_allow_html=True)
        all_cols = current_df.columns.tolist()
        num_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1: 
            col_date = st.selectbox("Select Timeline Axis Column", all_cols)
        with col_f2: 
            col_val = st.selectbox("Select Target Variable to Forecast", num_cols)
        with col_f3: 
            time_freq = st.selectbox("Frequency Window", options=[("Daily", "D"), ("Weekly", "W"), ("Monthly", "M")], format_func=lambda x: x[0])
        horizon = st.slider("Prediction Horizon Steps", 1, 24, 6)
        
        if st.button("Generate Analytical Forecasting Analytics", use_container_width=True):
            try:
                with st.spinner("🔮 Running ARIMA analysis..."):
                    forecast_data, forecast_insights = DataTriageEngine.generate_forecast(current_df, col_date, col_val, periods=horizon, freq=time_freq[1])
                    log_action(f"ARIMA Forecast Run on '{col_val}' for {horizon} intervals.")
                    UIComponents.render_forecast_dashboard(forecast_data, col_val, forecast_insights)
            except Exception as e: 
                st.error(f"⚠️ Time-Series Pipeline Failure: {e}")

    elif "🗂️" in feature_choice:
        pivot_header = """
        <div class="custom-card" style="margin-bottom: 16px;">
            <h4 style="margin: 0; color: #f1f5f9;">Pivot Table Analyzer</h4>
            <p style="margin: 8px 0 0 0; color: #cbd5e1; font-size: 13px;">Aggregate and summarize data with custom pivot operations</p>
        </div>
        """
        st.markdown(pivot_header, unsafe_allow_html=True)
        all_cols = current_df.columns.tolist()
        num_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            pivot_row = st.selectbox("Group By (Rows)", all_cols)
        with col_p2:
            pivot_val = st.selectbox("Target Calculation Field", num_cols)
        with col_p3:
            math_operation = st.selectbox("Aggregation Metric", ["sum", "mean", "count", "max", "min"])
        
        if st.button("Generate Pivot Aggregations", use_container_width=True):
            st.dataframe(DataTriageEngine.build_pivot_table(current_df, pivot_row, pivot_val, math_operation), use_container_width=True)

    elif "🤝" in feature_choice:
        merge_header = """
        <div class="custom-card" style="margin-bottom: 16px;">
            <h4 style="margin: 0; color: #f1f5f9;">Client Consolidation Merger</h4>
            <p style="margin: 8px 0 0 0; color: #cbd5e1; font-size: 13px;">Combine duplicate entries and flatten hierarchical data</p>
        </div>
        """
        st.markdown(merge_header, unsafe_allow_html=True)
        all_columns = current_df.columns.tolist()
        numeric_columns = current_df.select_dtypes(include=[np.number]).columns.tolist()
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            merge_target = st.selectbox("Select column with repeating labels", all_columns)
        with col_m2:
            value_target = st.selectbox("Select numeric column to combine", numeric_columns)
        with col_m3:
            math_strategy = st.selectbox("Strategy", ["sum", "mean", "max", "count"])
        
        if st.button("Run Consolidation", use_container_width=True):
            st.session_state.working_df = DataTriageEngine.aggregate_and_collapse(current_df, merge_target, value_target, math_strategy)
            st.success("✅ Dataset successfully flattened!")
            st.rerun()
            
    elif "🧠" in feature_choice:
        ml_header = """
        <div class="custom-card" style="margin-bottom: 16px;">
            <h4 style="margin: 0; color: #f1f5f9;">Automated Machine Learning Studio</h4>
            <p style="margin: 8px 0 0 0; color: #cbd5e1; font-size: 13px;">Train predictive models and run interactive what-if simulations</p>
        </div>
        """
        st.markdown(ml_header, unsafe_allow_html=True)
        all_cols = current_df.columns.tolist()
        col_m1, col_m2 = st.columns(2)
        with col_m1: 
            target_var = st.selectbox("Select Target Label", all_cols, index=len(all_cols)-1)
        with col_m2: 
            selected_features = st.multiselect("Select Feature Dimensions", all_cols, default=[c for c in all_cols if c != target_var])

        if len(selected_features) > 0 and st.button("Train Automated Machine Learning Model", use_container_width=True):
            try:
                with st.spinner("🤖 Processing forest pipelines..."):
                    st.session_state.trained_ml_data = DataTriageEngine.run_machine_learning_pipeline(current_df, target_var, selected_features)
                    log_action(f"ML Studio Model Trained on '{target_var}'.")
                    st.success("✅ Model trained successfully!")
            except Exception as e: 
                st.error(f"⚠️ Training Interrupted: {e}")

        if st.session_state.trained_ml_data is not None:
            res = st.session_state.trained_ml_data
            st.markdown("---")
            
            results_header = f"""
            <div style="
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(99, 102, 241, 0.1) 100%);
                border-left: 4px solid #10b981;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 20px;
            ">
                <h2 style="margin: 0; color: #f1f5f9;">🎉 Pipeline Execution Results: {res['task_type']} Engine</h2>
            </div>
            """
            st.markdown(results_header, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1: 
                UIComponents.render_stat_card(
                    res["score_metric"],
                    f"{res['score_value']}",
                    "🎯",
                    "success"
                )
            with c2: 
                if res["error_value"] is None:
                    UIComponents.render_stat_card(
                        "Evaluation Strategy",
                        "Cross-Validation",
                        "✓",
                        "primary"
                    )
                else:
                    UIComponents.render_stat_card(
                        "Mean Absolute Error",
                        f"{res['error_value']:.4f}",
                        "📊",
                        "warning"
                    )
            
            # Render our performance analytics tracking line graph
            UIComponents.render_ml_performance_chart(res["preview_df"])
            
            ch1, ch2 = st.columns([1, 1])
            with ch1: 
                feature_header = """
                <div class="custom-card" style="margin-bottom: 12px;">
                    <h4 style="margin: 0; color: #f1f5f9;">📊 Feature Importance Ranking</h4>
                </div>
                """
                st.markdown(feature_header, unsafe_allow_html=True)
                st.bar_chart(data=res["feature_importance"], x="Feature Vector", y="Significance Weight")
            with ch2: 
                preview_header = """
                <div class="custom-card" style="margin-bottom: 12px;">
                    <h4 style="margin: 0; color: #f1f5f9;">🎯 Prediction Sample Preview</h4>
                </div>
                """
                st.markdown(preview_header, unsafe_allow_html=True)
                st.dataframe(res["preview_df"].head(5), use_container_width=True)
                
            # Render our modular simulation dashboard element
            UIComponents.render_what_if_canvas(current_df, res)
else:
    empty_state_html = """
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 60vh;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(236, 72, 153, 0.05) 100%);
        border: 2px dashed rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        text-align: center;
    ">
        <div style="font-size: 64px; margin-bottom: 20px;">📤</div>
        <h2 style="margin: 0 0 12px 0; color: #f1f5f9; font-size: 24px;">Ready to Clean Your Data</h2>
        <p style="margin: 0; color: #cbd5e1; font-size: 14px; max-width: 400px; line-height: 1.6;">
            Upload a CSV file in the sidebar to begin. The system will automatically analyze your dataset and prepare it for processing.
        </p>
    </div>
    """
    st.markdown(empty_state_html, unsafe_allow_html=True)
  