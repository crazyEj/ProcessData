import streamlit as st
import pandas as pd
import numpy as np

class UIComponents:
    """
    Dedicated layout file handling major interactive canvas 
    and dashboard visual assemblies.
    """
    
    @staticmethod
    def inject_custom_css():
        """Injects custom CSS for enhanced aesthetic appeal with hover effects."""
        custom_css = """
        <style>
        /* Global Styling */
        :root {
            --primary: #B8956A;
            --primary-dark: #9F7F5C;
            --secondary: #94A3B8;
            --success: #22C55E;
            --warning: #F59E0B;
            --danger: #EF4444;
            --bg: #0F172A;
            --bg-alt: #111827;
            --card-bg: #1E293B;
            --border: rgba(148, 163, 184, 0.3);
            --text: #E2E8F0;
            --text-muted: #94A3B8;
            --accent: #FBBF24;
        }

        html, body, .block-container, .main {
            background: radial-gradient(circle at top left, rgba(59, 130, 246, 0.12), transparent 20%),
                        linear-gradient(180deg, var(--bg) 0%, var(--bg-alt) 100%);
            color: var(--text);
        }

        .css-1d391kg {
            background-color: transparent !important;
        }

        /* Custom Card Styling */
        .custom-card {
            background: linear-gradient(180deg, #16213A 0%, #0F172A 100%);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            margin: 12px 0;
            transition: transform 0.25s ease, box-shadow 0.25s ease;
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.25);
        }

        .custom-card:hover {
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.35);
            transform: translateY(-3px);
        }

        /* Metric Card Styling */
        .metric-card {
            background: #111827;
            border-left: 4px solid var(--primary);
            border-radius: 16px;
            padding: 18px;
            margin: 10px 0;
            transition: transform 0.25s ease, box-shadow 0.25s ease;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
        }

        .metric-card:hover {
            box-shadow: 0 14px 36px rgba(0, 0, 0, 0.26);
            transform: translateX(4px);
        }

        /* Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary) 0%, #9B7A57 100%);
            border: none;
            border-radius: 14px;
            color: #F8FAFC;
            font-weight: 700;
            padding: 11px 20px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            box-shadow: 0 10px 25px rgba(59, 130, 246, 0.2);
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #A57D4B 0%, #8A6B46 100%);
            box-shadow: 0 14px 30px rgba(59, 130, 246, 0.28);
            transform: translateY(-2px);
        }

        .stButton > button:active {
            transform: translateY(0px);
        }

        /* Input Styling */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        .stDateInput > div > div > input {
            background-color: #0F172A !important;
            border: 1px solid rgba(148, 163, 184, 0.25) !important;
            border-radius: 12px !important;
            color: var(--text) !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
            padding: 10px !important;
        }

        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stNumberInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: rgba(251, 191, 36, 0.55) !important;
            box-shadow: 0 0 0 4px rgba(251, 191, 36, 0.15) !important;
        }

        /* Alert Styling */
        .stAlert {
            border-radius: 14px;
            border: 1px solid rgba(148, 163, 184, 0.24);
            background: rgba(15, 23, 42, 0.92) !important;
            color: var(--text) !important;
        }

        .stInfo {
            background-color: rgba(56, 189, 248, 0.08) !important;
            border-color: rgba(56, 189, 248, 0.3) !important;
            color: var(--text) !important;
        }

        .stSuccess {
            background-color: rgba(34, 197, 94, 0.12) !important;
            border-color: rgba(34, 197, 94, 0.3) !important;
            color: var(--text) !important;
        }

        .stWarning {
            background-color: rgba(245, 158, 11, 0.12) !important;
            border-color: rgba(245, 158, 11, 0.3) !important;
            color: var(--text) !important;
        }

        .stError {
            background-color: rgba(239, 68, 68, 0.12) !important;
            border-color: rgba(239, 68, 68, 0.3) !important;
            color: var(--text) !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #111827 0%, #0F172A 100%);
            border-right: 1px solid rgba(148, 163, 184, 0.18);
            color: var(--text);
        }

        [data-testid="stSidebar"] .css-1d391kg {
            background: transparent !important;
        }

        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > [style*="flex-direction"] > button {
            margin: 6px 0;
        }

        [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {
            color: var(--text) !important;
        }

        /* Dataframe Styling */
        .stDataFrame {
            border-radius: 16px;
            overflow: hidden;
            background: #0F172A !important;
        }

        /* Header Styling */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text);
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.45);
        }

        /* Markdown Styling */
        .stMarkdown {
            font-size: 14px;
            line-height: 1.7;
            color: var(--text);
        }

        .stMarkdown p, .stMarkdown span, .stMarkdown div {
            color: var(--text) !important;
        }

        .stMarkdown a {
            color: var(--primary) !important;
        }

        /* Divider */
        hr {
            border-color: rgba(148, 163, 184, 0.18);
            margin: 24px 0;
        }

        /* Animation Classes */
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .fade-in {
            animation: fadeIn 0.5s ease-in;
        }

        .slide-in {
            animation: slideIn 0.5s ease-out;
        }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)

    @staticmethod
    def render_stat_card(label: str, value: str, icon: str = "📊", color: str = "primary"):
        """Renders a styled stat card with icon and hover effect."""
        color_map = {
            "primary": "#B8956A",
            "success": "#8B7355",
            "warning": "#A68A74",
            "danger": "#6D5C50",
            "secondary": "#7E6D5C"
        }
        
        hex_color = color_map.get(color, "#B8956A")
        card_html = f"""
        <div style="
            background: linear-gradient(135deg, #FFFFFF 0%, #F5F0EB 100%);
            border-left: 4px solid {hex_color};
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
            transition: all 0.3s ease;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(184, 149, 106, 0.1);
        " onmouseover="this.style.boxShadow='0 4px 12px rgba(184, 149, 106, 0.2)'; this.style.transform='translateX(4px)'" 
           onmouseout="this.style.boxShadow='0 2px 8px rgba(184, 149, 106, 0.1)'; this.style.transform='translateX(0)'">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <p style="margin: 0; color: #5C4A42; font-size: 12px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">{label}</p>
                    <p style="margin: 8px 0 0 0; color: #3C2A23; font-size: 24px; font-weight: bold;">{value}</p>
                </div>
                <span style="font-size: 32px;">{icon}</span>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    @staticmethod
    def render_forecast_dashboard(forecast_data, col_val, insights=None):
        st.markdown("---")
        
        # --- AI ANALYST INSIGHTS CARD ---
        if insights:
            change_sign = "+" if insights["pct_change"] >= 0 else ""
            change_icon = "📈" if insights["pct_change"] >= 0 else "📉"
            
            insights_html = f"""
            <div class="custom-card" style="border-left: 4px solid #B8956A;">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                    <span style="font-size: 28px;">💡</span>
                    <h3 style="margin: 0; color: #3C2A23;">AI Analyst Market Alert</h3>
                </div>
                <div style="background: rgba(184, 149, 106, 0.1); border-radius: 6px; padding: 12px; margin-bottom: 12px; border-left: 3px solid #B8956A;">
                    <p style="margin: 0; color: #5C4A42; line-height: 1.6;">
                        The ARIMA engine predicts that <strong style="color: #3C2A23;">{insights['target_name']}</strong> will 
                        <strong style="color: #8B7355;">{insights['direction']} by {change_sign}{insights['pct_change']}%</strong> over the next {insights['horizon_steps']} intervals.
                    </p>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div style="background: rgba(109, 92, 80, 0.1); padding: 10px; border-radius: 6px; border-left: 3px solid #6D5C50;">
                        <p style="margin: 0; color: #5C4A42; font-size: 11px; text-transform: uppercase;">Worst-Case Floor</p>
                        <p style="margin: 4px 0 0 0; color: #6D5C50; font-weight: bold; font-size: 16px;">₱ {insights['worst_case_floor']:,.2f}</p>
                    </div>
                    <div style="background: rgba(139, 115, 85, 0.1); padding: 10px; border-radius: 6px; border-left: 3px solid #8B7355;">
                        <p style="margin: 0; color: #5C4A42; font-size: 11px; text-transform: uppercase;">Best-Case Ceiling</p>
                        <p style="margin: 4px 0 0 0; color: #8B7355; font-weight: bold; font-size: 16px;">₱ {insights['best_case_ceiling']:,.2f}</p>
                    </div>
                </div>
            </div>
            """
            st.markdown(insights_html, unsafe_allow_html=True)
        
        st.write(f"#### 📊 High-Tier Valuation Forecasting Chart: {col_val}")
        st.line_chart(
            data=forecast_data, 
            x="Timeline Axis", 
            y=["Historical Value", "Predicted Value", "Lower Bound Price", "Upper Bound Price"]
        )
        
        c_card1, c_card2, c_card3 = st.columns(3)
        with c_card1: 
            UIComponents.render_stat_card(
                "Likely Future Target",
                f"₱ {forecast_data['Predicted Value'].dropna().iloc[-1]:,.2f}",
                "🎯",
                "primary"
            )
        with c_card2: 
            UIComponents.render_stat_card(
                "Worst-Case Bound (95%)",
                f"₱ {forecast_data['Lower Bound Price'].dropna().iloc[-1]:,.2f}",
                "📉",
                "danger"
            )
        with c_card3: 
            UIComponents.render_stat_card(
                "Best-Case Bound (95%)",
                f"₱ {forecast_data['Upper Bound Price'].dropna().iloc[-1]:,.2f}",
                "📈",
                "success"
            )
        st.dataframe(forecast_data, use_container_width=True)

    @staticmethod
    def render_ml_performance_chart(preview_df):
        """
        Renders an 'Actual vs. Predicted' performance comparison chart
        with enhanced styling.
        """
        chart_html = """
        <div class="custom-card">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 16px;">
                <span style="font-size: 24px;">📉</span>
                <h3 style="margin: 0; color: #3C2A23;">Performance Tracking: Actual vs. Model Prediction</h3>
            </div>
            <p style="margin: 0 0 12px 0; color: #5C4A42; font-size: 13px;">
                This visualization maps the true target values directly against the model's computed guesses to show prediction accuracy.
            </p>
        </div>
        """
        st.markdown(chart_html, unsafe_allow_html=True)
        st.line_chart(preview_df, y=["Actual Value", "Model Prediction"])

    @staticmethod
    def render_what_if_canvas(current_df, res):
        st.markdown("---")
        
        canvas_header = """
        <div class="custom-card">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <span style="font-size: 28px;">🔮</span>
                <div>
                    <h3 style="margin: 0; color: #3C2A23;">Live 'What-If' Simulation Canvas</h3>
                    <p style="margin: 4px 0 0 0; color: #5C4A42; font-size: 13px;">Adjust the parameters below to see calculations in real-time.</p>
                </div>
            </div>
        </div>
        """
        st.markdown(canvas_header, unsafe_allow_html=True)
        
        sim_inputs = {}
        input_cols = st.columns(len(res["feature_cols"]))
        
        for idx, col_name in enumerate(res["feature_cols"]):
            with input_cols[idx]:
                if np.issubdtype(current_df[col_name].dtype, np.number):
                    min_v = float(current_df[col_name].min())
                    max_v = float(current_df[col_name].max())
                    mean_v = float(current_df[col_name].median())
                    sim_inputs[col_name] = st.slider(f"{col_name}", min_value=min_v, max_value=max_v, value=mean_v)
                else:
                    unique_options = current_df[col_name].dropna().unique().astype(str).tolist()
                    sim_inputs[col_name] = st.selectbox(f"{col_name}", options=unique_options)
        
        try:
            input_df = pd.DataFrame([sim_inputs])
            for col_name in res["feature_cols"]:
                if col_name in res["encoders"]:
                    le = res["encoders"][col_name]
                    val_str = str(input_df.loc[0, col_name])
                    input_df.loc[0, col_name] = le.transform([val_str])[0] if val_str in le.classes_ else 0
                        
            raw_pred = res["model_object"].predict(input_df)[0]
            
            if res["task_type"] == "Classification" and "_target" in res["encoders"]:
                final_prediction = res["encoders"]["_target"].inverse_transform([int(raw_pred)])[0]
                prediction_html = f"""
                <div style="
                    background: linear-gradient(135deg, rgba(139, 115, 85, 0.1) 0%, rgba(184, 149, 106, 0.1) 100%);
                    border-left: 4px solid #8B7355;
                    border-radius: 8px;
                    padding: 16px;
                    margin-top: 20px;
                    text-align: center;
                ">
                    <p style="margin: 0; color: #5C4A42; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Simulated Prediction</p>
                    <h2 style="margin: 12px 0 0 0; color: #8B7355; font-weight: bold;">🔮 {final_prediction}</h2>
                    <p style="margin: 8px 0 0 0; color: #5C4A42; font-size: 12px;">Target: {res['target_col']}</p>
                </div>
                """
                st.markdown(prediction_html, unsafe_allow_html=True)
            else:
                prediction_html = f"""
                <div style="
                    background: linear-gradient(135deg, rgba(184, 149, 106, 0.1) 0%, rgba(159, 127, 92, 0.1) 100%);
                    border-left: 4px solid #B8956A;
                    border-radius: 8px;
                    padding: 16px;
                    margin-top: 20px;
                    text-align: center;
                ">
                    <p style="margin: 0; color: #5C4A42; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Simulated Prediction</p>
                    <h2 style="margin: 12px 0 0 0; color: #B8956A; font-weight: bold;">🔮 ₱ {raw_pred:,.2f}</h2>
                    <p style="margin: 8px 0 0 0; color: #5C4A42; font-size: 12px;">Estimated Target: {res['target_col']}</p>
                </div>
                """
                st.markdown(prediction_html, unsafe_allow_html=True)
        except Exception as sim_err:
            st.error(f"⚠️ Awaiting model configuration vectors... {sim_err}")