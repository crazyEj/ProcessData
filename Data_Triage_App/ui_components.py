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
            --secondary: #7E6D5C;
            --success: #8B7355;
            --warning: #A68A74;
            --danger: #6D5C50;
            --light-bg: #F5F0EB;
            --card-bg: #E8D5C4;
            --border: #B8956A;
            --text-dark: #3C2A23;
            --text-dim: #5C4A42;
        }

        /* Main Container */
        .main {
            background: linear-gradient(135deg, #F5F0EB 0%, #E8D5C4 100%);
        }

        /* Custom Card Styling */
        .custom-card {
            background: linear-gradient(135deg, #FFFFFF 0%, #F5F0EB 100%);
            border: 1px solid rgba(184, 149, 106, 0.4);
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 15px rgba(184, 149, 106, 0.15);
        }

        .custom-card:hover {
            border-color: rgba(184, 149, 106, 0.8);
            box-shadow: 0 8px 25px rgba(184, 149, 106, 0.25);
            transform: translateY(-4px);
            background: linear-gradient(135deg, #F5F0EB 0%, #E8D5C4 100%);
        }

        /* Metric Card Styling */
        .metric-card {
            background: linear-gradient(135deg, #FFFFFF 0%, #F5F0EB 100%);
            border-left: 4px solid #B8956A;
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(184, 149, 106, 0.1);
        }

        .metric-card:hover {
            border-left-color: #8B7355;
            box-shadow: 0 4px 12px rgba(184, 149, 106, 0.2);
            transform: translateX(4px);
        }

        /* Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, #B8956A 0%, #9F7F5C 100%);
            border: none;
            border-radius: 8px;
            color: #FFFFFF;
            font-weight: 600;
            padding: 10px 20px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(184, 149, 106, 0.3);
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #9F7F5C 0%, #8B7355 100%);
            box-shadow: 0 6px 20px rgba(184, 149, 106, 0.5);
            transform: translateY(-2px);
        }

        .stButton > button:active {
            transform: translateY(0px);
        }

        /* Input Styling */
        .stTextInput > div > div > input,
        .stSlider > div > div > div,
        .stSelectbox > div > div > select {
            background-color: #FFFFFF !important;
            border: 1px solid rgba(184, 149, 106, 0.4) !important;
            border-radius: 8px !important;
            color: #3C2A23 !important;
            transition: all 0.3s ease !important;
            padding: 10px !important;
        }

        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #B8956A !important;
            box-shadow: 0 0 0 3px rgba(184, 149, 106, 0.15) !important;
        }

        /* Alert Styling */
        .stAlert {
            border-radius: 8px;
            border: 1px solid;
            backdrop-filter: blur(10px);
        }

        .stInfo {
            background-color: rgba(184, 149, 106, 0.1) !important;
            border-color: rgba(184, 149, 106, 0.3) !important;
            color: #3C2A23 !important;
        }

        .stSuccess {
            background-color: rgba(139, 115, 85, 0.1) !important;
            border-color: rgba(139, 115, 85, 0.3) !important;
            color: #3C2A23 !important;
        }

        .stWarning {
            background-color: rgba(166, 138, 116, 0.1) !important;
            border-color: rgba(166, 138, 116, 0.3) !important;
            color: #3C2A23 !important;
        }

        .stError {
            background-color: rgba(109, 92, 80, 0.1) !important;
            border-color: rgba(109, 92, 80, 0.3) !important;
            color: #3C2A23 !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #F5F0EB 0%, #E8D5C4 100%);
            border-right: 1px solid rgba(184, 149, 106, 0.3);
        }

        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > [style*="flex-direction"] > button {
            margin: 5px 0;
        }

        /* Dataframe Styling */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
        }

        /* Header Styling */
        h1, h2, h3, h4, h5, h6 {
            color: #3C2A23;
            text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
        }

        /* Markdown Styling */
        .stMarkdown {
            font-size: 14px;
            line-height: 1.6;
            color: #3C2A23;
        }

        /* Divider */
        hr {
            border-color: rgba(184, 149, 106, 0.3);
            margin: 20px 0;
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