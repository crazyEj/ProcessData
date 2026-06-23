import streamlit as st
import pandas as pd
import numpy as np

class UIComponents:
    """
    Dedicated layout file handling major interactive canvas 
    and dashboard visual assemblies.
    """
    
    @staticmethod
    def render_forecast_dashboard(forecast_data, col_val, insights=None):
        st.markdown("---")
        
        # --- NEW: AUTOMATED EXPLANATORY INSIGHTS CARD ---
        if insights:
            change_sign = "+" if insights["pct_change"] >= 0 else ""
            st.info(
                f"💡 **AI Analyst Market Alert:**\n\n"
                f"The ARIMA engine predicts that **{insights['target_name']}** will "
                f"**{insights['direction']} by {change_sign}{insights['pct_change']}%** over the next {insights['horizon_steps']} intervals. "
                f"The worst-case floor threshold is calculated at **₱ {insights['worst_case_floor']:,.2f}**, "
                f"while the optimal ceiling capacity boundary scales up to **₱ {insights['best_case_ceiling']:,.2f}**."
            )
        # ------------------------------------------------
        
        st.write(f"#### 📊 High-Tier Valuation Forecasting Chart: {col_val}")
        st.line_chart(
            data=forecast_data, 
            x="Timeline Axis", 
            y=["Historical Value", "Predicted Value", "Lower Bound Price", "Upper Bound Price"]
        )
        
        c_card1, c_card2, c_card3 = st.columns(3)
        with c_card1: 
            st.metric(label="Likely Future Target Valuation", value=f"₱ {forecast_data['Predicted Value'].dropna().iloc[-1]:,.2f}")
        with c_card2: 
            st.metric(label="Worst-Case Bound Price Threshold (95%)", value=f"₱ {forecast_data['Lower Bound Price'].dropna().iloc[-1]:,.2f}")
        with c_card3: 
            st.metric(label="Best-Case Bound Price Threshold (95%)", value=f"₱ {forecast_data['Upper Bound Price'].dropna().iloc[-1]:,.2f}")
        st.dataframe(forecast_data, use_container_width=True)

    @staticmethod
    def render_ml_performance_chart(preview_df):
        """
        New: Renders an 'Actual vs. Predicted' performance comparison chart
        to show the before/after tracking precision.
        """
        st.write("#### 📉 Performance Tracking: Actual vs. Model Prediction")
        st.caption("This visualization maps the true target values directly against the model's computed guesses to show prediction accuracy.")
        st.line_chart(preview_df, y=["Actual Value", "Model Prediction"])

    @staticmethod
    def render_what_if_canvas(current_df, res):
        st.markdown("---")
        st.write("### 🔮 Live 'What-If' Simulation Canvas")
        st.caption("Adjust the parameters below to see calculations in real-time.")
        
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
                st.success(f"🔮 **Live Simulated Prediction Output:** `{res['target_col']}` = **{final_prediction}**")
            else:
                st.success(f"🔮 **Live Simulated Prediction Output:** `{res['target_col']}` = **₱ {raw_pred:,.2f}**")
        except Exception as sim_err:
            st.caption(f"Awaiting model configuration vectors... {sim_err}")