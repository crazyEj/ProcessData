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
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --secondary: #ec4899;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --dark-bg: #0f172a;
            --card-bg: #1e293b;
            --border: #334155;
            --text-light: #f1f5f9;
            --text-dim: #cbd5e1;
        }

        /* Main Container */
        .main {
            background: linear-gradient(135deg, #0f172a 0%, #1a1f3a 100%);
        }

        /* Custom Card Styling */
        .custom-card {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }

        .custom-card:hover {
            border-color: rgba(99, 102, 241, 0.6);
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.2);
            transform: translateY(-4px);
            background: linear-gradient(135deg, #334155 0%, #475569 100%);
        }

        /* Metric Card Styling */
        .metric-card {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-left: 4px solid #6366f1;
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
            transition: all 0.3s ease;
        }

        .metric-card:hover {
            border-left-color: #ec4899;
            box-shadow: 0 4px 12px rgba(236, 72, 153, 0.2);
            transform: translateX(4px);
        }

        /* Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
            border: none;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            padding: 10px 20px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
            transform: translateY(-2px);
        }

        .stButton > button:active {
            transform: translateY(0px);
        }

        /* Input Styling */
        .stTextInput > div > div > input,
        .stSlider > div > div > div,
        .stSelectbox > div > div > select {
            background-color: #334155 !important;
            border: 1px solid rgba(99, 102, 241, 0.3) !important;
            border-radius: 8px !important;
            color: #f1f5f9 !important;
            transition: all 0.3s ease !important;
            padding: 10px !important;
        }

        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
        }

        /* Alert Styling */
        .stAlert {
            border-radius: 8px;
            border: 1px solid;
            backdrop-filter: blur(10px);
        }

        .stInfo {
            background-color: rgba(99, 102, 241, 0.1) !important;
            border-color: rgba(99, 102, 241, 0.3) !important;
        }

        .stSuccess {
            background-color: rgba(16, 185, 129, 0.1) !important;
            border-color: rgba(16, 185, 129, 0.3) !important;
        }

        .stWarning {
            background-color: rgba(245, 158, 11, 0.1) !important;
            border-color: rgba(245, 158, 11, 0.3) !important;
        }

        .stError {
            background-color: rgba(239, 68, 68, 0.1) !important;
            border-color: rgba(239, 68, 68, 0.3) !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1a1f3a 100%);
            border-right: 1px solid rgba(99, 102, 241, 0.2);
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
            color: #f1f5f9;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }

        /* Markdown Styling */
        .stMarkdown {
            font-size: 14px;
            line-height: 1.6;
        }

        /* Divider */
        hr {
            border-color: rgba(99, 102, 241, 0.2);
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
            "primary": "#6366f1",
            "success": "#10b981",
            "warning": "#f59e0b",
            "danger": "#ef4444",
            "secondary": "#ec4899"
        }
        
        hex_color = color_map.get(color, "#6366f1")
        card_html = f"""
        <div style="
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-left: 4px solid {hex_color};
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
            transition: all 0.3s ease;
            cursor: pointer;
        " onmouseover="this.style.boxShadow='0 4px 12px rgba({int(hex_color[1:3], 16)}, {int(hex_color[3:5], 16)}, {int(hex_color[5:7], 16)}, 0.3)'; this.style.transform='translateX(4px)'" 
           onmouseout="this.style.boxShadow='none'; this.style.transform='translateX(0)'">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <p style="margin: 0; color: #cbd5e1; font-size: 12px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">{label}</p>
                    <p style="margin: 8px 0 0 0; color: #f1f5f9; font-size: 24px; font-weight: bold;">{value}</p>
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
            <div class="custom-card" style="border-left: 4px solid #6366f1;">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                    <span style="font-size: 28px;">💡</span>
                    <h3 style="margin: 0; color: #f1f5f9;">AI Analyst Market Alert</h3>
                </div>
                <div style="background: rgba(99, 102, 241, 0.1); border-radius: 6px; padding: 12px; margin-bottom: 12px; border-left: 3px solid #6366f1;">
                    <p style="margin: 0; color: #cbd5e1; line-height: 1.6;">
                        The ARIMA engine predicts that <strong style="color: #f1f5f9;">{insights['target_name']}</strong> will 
                        <strong style="color: #ec4899;">{insights['direction']} by {change_sign}{insights['pct_change']}%</strong> over the next {insights['horizon_steps']} intervals.
                    </p>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div style="background: rgba(239, 68, 68, 0.1); padding: 10px; border-radius: 6px; border-left: 3px solid #ef4444;">
                        <p style="margin: 0; color: #cbd5e1; font-size: 11px; text-transform: uppercase;">Worst-Case Floor</p>
                        <p style="margin: 4px 0 0 0; color: #ef4444; font-weight: bold; font-size: 16px;">₱ {insights['worst_case_floor']:,.2f}</p>
                    </div>
                    <div style="background: rgba(16, 185, 129, 0.1); padding: 10px; border-radius: 6px; border-left: 3px solid #10b981;">
                        <p style="margin: 0; color: #cbd5e1; font-size: 11px; text-transform: uppercase;">Best-Case Ceiling</p>
                        <p style="margin: 4px 0 0 0; color: #10b981; font-weight: bold; font-size: 16px;">₱ {insights['best_case_ceiling']:,.2f}</p>
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
                <h3 style="margin: 0; color: #f1f5f9;">Performance Tracking: Actual vs. Model Prediction</h3>
            </div>
            <p style="margin: 0 0 12px 0; color: #cbd5e1; font-size: 13px;">
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
                    <h3 style="margin: 0; color: #f1f5f9;">Live 'What-If' Simulation Canvas</h3>
                    <p style="margin: 4px 0 0 0; color: #cbd5e1; font-size: 13px;">Adjust the parameters below to see calculations in real-time.</p>
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
                    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(99, 102, 241, 0.1) 100%);
                    border-left: 4px solid #10b981;
                    border-radius: 8px;
                    padding: 16px;
                    margin-top: 20px;
                    text-align: center;
                ">
                    <p style="margin: 0; color: #cbd5e1; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Simulated Prediction</p>
                    <h2 style="margin: 12px 0 0 0; color: #10b981; font-weight: bold;">🔮 {final_prediction}</h2>
                    <p style="margin: 8px 0 0 0; color: #cbd5e1; font-size: 12px;">Target: {res['target_col']}</p>
                </div>
                """
                st.markdown(prediction_html, unsafe_allow_html=True)
            else:
                prediction_html = f"""
                <div style="
                    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
                    border-left: 4px solid #6366f1;
                    border-radius: 8px;
                    padding: 16px;
                    margin-top: 20px;
                    text-align: center;
                ">
                    <p style="margin: 0; color: #cbd5e1; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Simulated Prediction</p>
                    <h2 style="margin: 12px 0 0 0; color: #6366f1; font-weight: bold;">🔮 ₱ {raw_pred:,.2f}</h2>
                    <p style="margin: 8px 0 0 0; color: #cbd5e1; font-size: 12px;">Estimated Target: {res['target_col']}</p>
                </div>
                """
                st.markdown(prediction_html, unsafe_allow_html=True)
        except Exception as sim_err:
            st.error(f"⚠️ Awaiting model configuration vectors... {sim_err}")