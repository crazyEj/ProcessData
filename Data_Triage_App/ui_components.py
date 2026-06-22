import streamlit as st
import pandas as pd
import numpy as np

class UIComponents:
    """
    Dedicated layout file handling major interactive canvas 
    and dashboard visual assemblies.
    """
    
    @staticmethod
    def render_forecast_dashboard(forecast_data, col_val):
        st.markdown("---")
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