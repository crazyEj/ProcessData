import streamlit as st
import pandas as pd
import numpy as np

class UIComponents:
    """
    Dedicated layout file handling Gemini-inspired Obsidian Dark aesthetic 
    interactive canvases and dashboard assemblies.
    """
    
    @staticmethod
    def inject_custom_css():
        """Injects a premium, sleek Gemini-inspired Obsidian Dark mode CSS layout."""
        custom_css = """
        <style>
        /* Global Space-Aesthetic Reset */
        :root {
            --bg-main: #080B10;
            --bg-card: #131722;
            --bg-card-hover: #181E2C;
            --border-glow: rgba(56, 189, 248, 0.15);
            --border-glow-hover: rgba(139, 92, 246, 0.35);
            --text-primary: #F3F4F6;
            --text-secondary: #9CA3AF;
            --accent-blue: #38BDF8;
            --accent-purple: #8B5CF6;
            --accent-emerald: #10B981;
            --accent-rose: #F43F5E;
        }

        /* Fluid Gradient Space Canvas Background */
        html, body, .block-container, .main {
            background: radial-gradient(circle at 0% 0%, rgba(139, 92, 246, 0.07), transparent 35%),
                        radial-gradient(circle at 100% 100%, rgba(56, 189, 248, 0.05), transparent 40%),
                        var(--bg-main) !important;
            color: var(--text-primary) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Container Overrides */
        .css-1d391kg, [data-testid="stHeader"] {
            background-color: transparent !important;
        }

        /* Frosted Glass Cyber Card */
        .custom-card {
            background: rgba(19, 23, 34, 0.65) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border-glow) !important;
            border-radius: 16px !important;
            padding: 24px !important;
            margin: 16px 0 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }

        .custom-card:hover {
            border-color: var(--border-glow-hover) !important;
            box-shadow: 0 15px 35px rgba(139, 92, 246, 0.1);
            transform: translateY(-2px);
        }

        /* Sleek Futuristic Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%) !important;
            border: none !important;
            border-radius: 12px !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            letter-spacing: 0.3px;
            padding: 12px 24px !important;
            transition: all 0.25s ease !important;
            box-shadow: 0 4px 15px rgba(124, 58, 237, 0.25) !important;
        }

        .stButton > button:hover {
            box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4) !important;
            transform: translateY(-1px);
            filter: brightness(1.1);
        }

        /* Modern Dark Input Fields */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        .stMultiSelect > div > div {
            background-color: #111520 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            color: var(--text-primary) !important;
            transition: all 0.2s ease !important;
        }

        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: var(--accent-blue) !important;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
        }

        /* Sidebar Styling Overhaul */
        [data-testid="stSidebar"] {
            background: #0B0E14 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        }

        /* Clean Dataframe Adjustments */
        .stDataFrame {
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            background-color: #0D111A !important;
        }

        /* Global Typography Cleanup */
        h1, h2, h3, h4, h5, h6, p, span, label {
            color: var(--text-primary) !important;
        }
        
        .stMarkdown p {
            color: var(--text-secondary) !important;
        }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)

    @staticmethod
    def render_stat_card(label: str, value: str, icon: str = "📊", color: str = "primary"):
        """Renders an Obsidian Dark metric block with specialized subtle color accent lines."""
        color_map = {
            "primary": "var(--accent-blue)",
            "success": "var(--accent-emerald)",
            "warning": "var(--accent-purple)",
            "danger": "var(--accent-rose)",
            "secondary": "var(--text-secondary)"
        }
        accent_line = color_map.get(color, "var(--accent-blue)")
        
        card_html = f"""
        <div class="custom-card" style="border-left: 3px solid {accent_line} !important; margin: 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <p style="margin: 0; color: var(--text-secondary) !important; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px;">{label}</p>
                    <p style="margin: 6px 0 0 0; color: var(--text-primary) !important; font-size: 22px; font-weight: 700; letter-spacing: -0.5px;">{value}</p>
                </div>
                <span style="font-size: 26px; opacity: 0.85;">{icon}</span>
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
            glow_accent = "var(--accent-emerald)" if insights["pct_change"] >= 0 else "var(--accent-rose)"
            
            insights_html = f"""
            <div class="custom-card" style="border-left: 4px solid var(--accent-purple) !important;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">
                    <span style="font-size: 24px;">✨</span>
                    <h3 style="margin: 0; font-size: 18px; font-weight: 600; letter-spacing: -0.3px;">AI Engine Analysis Insights</h3>
                </div>
                <div style="background: rgba(139, 92, 246, 0.06); border-radius: 10px; padding: 14px; margin-bottom: 14px; border: 1px solid rgba(139, 92, 246, 0.15);">
                    <p style="margin: 0; color: var(--text-primary) !important; line-height: 1.6; font-size: 14px;">
                        The predictive engine anticipates that <span style="color: var(--accent-blue) !important; font-weight: 600;">{insights['target_name']}</span> will 
                        <span style="color: {glow_accent} !important; font-weight: 600;">{insights['direction']} by {change_sign}{insights['pct_change']}%</span> across the scheduled horizon trajectory.
                    </p>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                    <div style="background: rgba(244, 63, 94, 0.04); padding: 12px; border-radius: 8px; border: 1px solid rgba(244, 63, 94, 0.1);">
                        <p style="margin: 0; color: var(--text-secondary) !important; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;">Worst-Case Boundary Floor</p>
                        <p style="margin: 4px 0 0 0; color: var(--accent-rose) !important; font-weight: 700; font-size: 16px;">₱ {insights['worst_case_floor']:,.2f}</p>
                    </div>
                    <div style="background: rgba(16, 185, 129, 0.04); padding: 12px; border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.1);">
                        <p style="margin: 0; color: var(--text-secondary) !important; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;">Optimal Capacity Ceiling</p>
                        <p style="margin: 4px 0 0 0; color: var(--accent-emerald) !important; font-weight: 700; font-size: 16px;">₱ {insights['best_case_ceiling']:,.2f}</p>
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
        
        st.write(" ")
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
                "success"
            )
        st.dataframe(forecast_data, use_container_width=True)

    @staticmethod
    def render_ml_performance_chart(preview_df):
        """Renders an 'Actual vs. Predicted' performance comparison chart wrapped in dark containers."""
        chart_html = """
        <div class="custom-card">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 22px;">📉</span>
                <h3 style="margin: 0; font-size: 16px; font-weight: 600;">Performance Tracking: Actual vs. Model Prediction</h3>
            </div>
            <p style="margin: 6px 0 0 0; color: var(--text-secondary) !important; font-size: 13px;">
                Direct alignment map matching historical training vectors against current production runtime estimations.
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
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 24px;">🔮</span>
                <div>
                    <h3 style="margin: 0; font-size: 18px; font-weight: 600;">Live Simulation Studio</h3>
                    <p style="margin: 4px 0 0 0; color: var(--text-secondary) !important; font-size: 13px;">Modify situational parameter metrics to evaluate runtime computational adjustments.</p>
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
                <div class="custom-card" style="border-top: 3px solid var(--accent-purple) !important; text-align: center; background: rgba(139, 92, 246, 0.03) !important;">
                    <p style="margin: 0; color: var(--text-secondary) !important; font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px;">Simulated Target Prediction</p>
                    <h2 style="margin: 8px 0; color: var(--accent-purple) !important; font-weight: 700; font-size: 26px; letter-spacing: -0.5px;">🔮 {final_prediction}</h2>
                    <p style="margin: 0; color: var(--text-secondary) !important; font-size: 12px;">Active Parameter Feature Workspace: {res['target_col']}</p>
                </div>
                """
                st.markdown(prediction_html, unsafe_allow_html=True)
            else:
                prediction_html = f"""
                <div class="custom-card" style="border-top: 3px solid var(--accent-blue) !important; text-align: center; background: rgba(56, 189, 248, 0.03) !important;">
                    <p style="margin: 0; color: var(--text-secondary) !important; font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px;">Simulated Valuation Matrix</p>
                    <h2 style="margin: 8px 0; color: var(--accent-blue) !important; font-weight: 700; font-size: 26px; letter-spacing: -0.5px;">🔮 ₱ {raw_pred:,.2f}</h2>
                    <p style="margin: 0; color: var(--text-secondary) !important; font-size: 12px;">Active Target Dimension: {res['target_col']}</p>
                </div>
                """
                st.markdown(prediction_html, unsafe_allow_html=True)
        except Exception as sim_err:
            st.caption(f"Awaiting validation model configuration vectors... {sim_err}")