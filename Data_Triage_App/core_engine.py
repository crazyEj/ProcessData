import pandas as pd
import numpy as np
from rapidfuzz import process, fuzz
from sklearn.ensemble import IsolationForest, RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, r2_score, mean_absolute_error
import re

class DataTriageEngine:
    """
    Core backend engine for handling structurally broken, missing, 
    and highly inconsistent datasets safely with embedded machine learning capabilities.
    """
    
    @staticmethod
    def robust_csv_import(file_buffer) -> pd.DataFrame:
        try:
            file_buffer.seek(0)
            df = pd.read_csv(file_buffer, on_bad_lines='skip', engine='python')
            file_buffer.seek(0)
            return df
        except Exception as e:
            raise RuntimeError(f"Structural collapse during parsing: {str(e)}")

    @staticmethod
    def get_health_metrics(df: pd.DataFrame) -> pd.DataFrame:
        metrics = []
        for col in df.columns:
            missing_count = df[col].isnull().sum()
            missing_pct = (missing_count / len(df)) * 100 if len(df) > 0 else 0
            inferred_types = df[col].dropna().apply(type).nunique()
            type_mismatch = "Yes (Mixed)" if inferred_types > 1 else "No (Clean)"
            
            metrics.append({
                "Column": col,
                "Inferred Type": str(df[col].dtype),
                "Missing Rows": missing_count,
                "Missing %": round(missing_pct, 2),
                "Type Mismatch": type_mismatch
            })
        return pd.DataFrame(metrics)
    @staticmethod
    def calculate_health_score(df: pd.DataFrame) -> int:
        """
        Computes a comprehensive percentage health score for the uploaded dataset.
        Deducts points dynamically based on null density and row duplication.
        """
        if df.empty:
            return 0
            
        total_cells = df.size
        total_nulls = df.isnull().sum().sum()
        
        # Calculate missing data penalty (0% nulls = 100% score component)
        null_ratio = total_nulls / total_cells if total_cells > 0 else 0
        null_score = (1 - null_ratio) * 100
        
        # Calculate duplication penalty (0 duplicated rows = 100% score component)
        duplicate_rows = df.duplicated().sum()
        dup_ratio = duplicate_rows / len(df) if len(df) > 0 else 0
        dup_score = (1 - dup_ratio) * 100
        
        # Weighted combination: 70% weight on data fullness, 30% on uniqueness
        final_score = int((null_score * 0.7) + (dup_score * 0.3))
        return max(0, min(100, final_score))

    @staticmethod
    def generate_demo_dataset() -> pd.DataFrame:
        """Returns a built-in sample data frame for demo and onboarding use."""
        sample_data = {
            "Order ID": [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
            "Region": ["North", "South", "East", "West", "North", "East", "South", "West"],
            "Sales": [450.0, 520.0, np.nan, 470.0, 610.0, 580.0, 495.0, np.nan],
            "Category": ["Office", "Furniture", "Office", "Furniture", "Technology", "Technology", "Office", "Furniture"],
            "Order Date": ["2026-01-15", "2026-02-03", "2026-02-20", "2026-03-07", "2026-03-18", "2026-04-01", "2026-04-12", "2026-04-20"],
            "Customer Name": ["Alpha Co", "Beta Ltd", "Gamma LLC", "Delta Inc", "Epsilon GmbH", "Zeta Co", "Eta Ltd", "Theta LLC"],
            "Status": ["Delivered", "Pending", "Delivered", "Canceled", "Delivered", "Pending", "Delivered", "Delivered"]
        }
        return pd.DataFrame(sample_data)

    @staticmethod
    def auto_impute(df: pd.DataFrame) -> pd.DataFrame:
        df_cleaned = df.copy()
        for col in df_cleaned.columns:
            if df_cleaned[col].isnull().sum() == 0:
                continue
            if np.issubdtype(df_cleaned[col].dtype, np.number):
                df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())
            else:
                if not df_cleaned[col].mode().empty:
                    df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mode()[0])
                else:
                    df_cleaned[col] = df_cleaned[col].fillna("Unknown")
        return df_cleaned

    @staticmethod
    def fuzzy_standardize(df: pd.DataFrame, column: str, base_word: str, threshold: float) -> tuple:
        df_cleaned = df.copy()
        unique_vals = df_cleaned[column].dropna().unique().astype(str).tolist()
        matches = process.extract(base_word, unique_vals, scorer=fuzz.WRatio, score_cutoff=threshold)
        words_to_replace = [match[0] for match in matches]
        if words_to_replace:
            df_cleaned[column] = df_cleaned[column].replace(words_to_replace, base_word)
        return df_cleaned, words_to_replace

    @staticmethod
    def isolate_anomalies(df: pd.DataFrame, num_columns: list, contamination: float) -> tuple:
        df_processed = df.copy()
        if not num_columns:
            return df_processed, 0
        temp_data = df_processed[num_columns].copy()
        for col in num_columns:
            temp_data[col] = temp_data[col].fillna(temp_data[col].median() if not temp_data[col].empty else 0)
        iso = IsolationForest(contamination=contamination, random_state=42)
        predictions = iso.fit_predict(temp_data)
        df_processed['Anomaly_Flag'] = np.where(predictions == -1, "⚠️ Malformed/Outlier", "✅ Normal")
        return df_processed, int((predictions == -1).sum())

    @staticmethod
    def global_deep_search(df: pd.DataFrame, query: str, use_regex: bool = False) -> pd.DataFrame:
        if not query:
            return df
        def row_search(row):
            for cell in row:
                if use_regex:
                    if re.search(query, str(cell), re.IGNORECASE): return True
                else:
                    if query.lower() in str(cell).lower(): return True
            return False
        return df[df.apply(row_search, axis=1)]

    @staticmethod
    def generate_forecast(df: pd.DataFrame, date_col: str, value_col: str, periods: int = 6, freq: str = 'M') -> tuple:
        from statsmodels.tsa.arima.model import ARIMA
        df_forecast = df.copy()
        df_forecast[date_col] = pd.to_datetime(df_forecast[date_col], errors='coerce')
        df_forecast[value_col] = pd.to_numeric(df_forecast[value_col], errors='coerce')
        df_forecast = df_forecast.dropna(subset=[date_col, value_col]).sort_values(by=date_col)
        df_forecast.set_index(date_col, inplace=True)
        ts_data = df_forecast[value_col].resample(freq).mean().ffill()
        
        # Fit ARIMA Model
        model = ARIMA(ts_data, order=(1, 1, 1))
        model_fitted = model.fit()
        forecast_res = model_fitted.get_forecast(steps=periods)
        
        forecast_values = forecast_res.predicted_mean
        confidence_intervals = forecast_res.conf_int(alpha=0.05)
        future_dates = pd.date_range(start=ts_data.index[-1], periods=periods + 1, freq=freq)[1:]
        
        historical_df = pd.DataFrame({
            "Timeline Axis": ts_data.index,
            "Historical Value": ts_data.values,
            "Predicted Value": np.nan,
            "Lower Bound Price": np.nan,
            "Upper Bound Price": np.nan
        })
        forecast_df = pd.DataFrame({
            "Timeline Axis": future_dates,
            "Historical Value": np.nan,
            "Predicted Value": forecast_values.values,
            "Lower Bound Price": confidence_intervals.iloc[:, 0].values,
            "Upper Bound Price": confidence_intervals.iloc[:, 1].values
        })
        
        # --- NEW: ANALYST INSIGHT GENERATION LOGIC ---
        last_historical = ts_data.values[-1] if len(ts_data.values) > 0 else 1
        final_forecast = forecast_values.values[-1]
        pct_change = ((final_forecast - last_historical) / last_historical) * 100
        
        insights = {
            "pct_change": round(pct_change, 1),
            "direction": "climb 📈" if pct_change >= 0 else "drop 📉",
            "final_predicted": final_forecast,
            "worst_case_floor": confidence_intervals.iloc[:, 0].values[-1],
            "best_case_ceiling": confidence_intervals.iloc[:, 1].values[-1],
            "target_name": value_col,
            "horizon_steps": periods
        }
        # ----------------------------------------------
        
        return pd.concat([historical_df, forecast_df], ignore_index=True), insights

    @staticmethod
    def build_pivot_table(df: pd.DataFrame, index_col: str, values_col: str, agg_func: str) -> pd.DataFrame:
        return pd.pivot_table(df.copy(), index=index_col, values=values_col, aggfunc=agg_func).sort_values(by=values_col, ascending=False).reset_index()

    @staticmethod
    def aggregate_and_collapse(df: pd.DataFrame, group_col: str, calc_col: str, strategy: str) -> pd.DataFrame:
        df_collapsed = df.copy()
        df_collapsed[calc_col] = pd.to_numeric(df_collapsed[calc_col], errors='coerce')
        return df_collapsed.groupby(group_col)[calc_col].agg(strategy).reset_index().sort_values(by=calc_col, ascending=False).reset_index(drop=True)

    @staticmethod
    def run_machine_learning_pipeline(df: pd.DataFrame, target_col: str, feature_cols: list) -> dict:
        """
        Upgraded type-safe pipeline: Handles strict pandas StringDtype arrays 
        and converts them to standard formats safely before encoding vectors.
        """
        working_df = df[feature_cols + [target_col]].copy().dropna(subset=[target_col])
        
        # --- Type-Safe Preprocessing Fix ---
        for col in feature_cols:
            # Force modern strict pandas StringDtype back to a standard object structure
            if isinstance(working_df[col].dtype, pd.StringDtype):
                working_df[col] = working_df[col].astype(object)
                
            if working_df[col].isnull().sum() > 0:
                if np.issubdtype(working_df[col].dtype, np.number):
                    working_df[col] = working_df[col].fillna(working_df[col].median())
                else:
                    working_df[col] = working_df[col].fillna("Unknown")

        X = working_df[feature_cols].copy()
        encoders = {}
        
        for col in X.columns:
            # Recheck type mappings to execute standard encoding loops
            if isinstance(X[col].dtype, pd.StringDtype):
                X[col] = X[col].astype(object)
                
            if not np.issubdtype(X[col].dtype, np.number):
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
                encoders[col] = le
        # -------------------------------------
                
        y = working_df[target_col]
        # Handle target data types cleanly if it's also a strict StringDtype
        if isinstance(y.dtype, pd.StringDtype):
            y = y.astype(object)
            
        is_classification = not np.issubdtype(y.dtype, np.number) or y.nunique() <= 10
        
        if is_classification:
            task_type = "Classification"
            le_target = LabelEncoder()
            y_encoded = le_target.fit_transform(y.astype(str))
            encoders["_target"] = le_target
            X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
            
            model = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train)
            predictions = model.predict(X_test)
            score_metric = "Accuracy Score"
            score_value = round(accuracy_score(y_test, predictions) * 100, 2)
            error_value = None
            y_test_orig = le_target.inverse_transform(y_test)
            pred_orig = le_target.inverse_transform(predictions)
        else:
            task_type = "Regression"
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            model = RandomForestRegressor(n_estimators=100, random_state=42).fit(X_train, y_train)
            predictions = model.predict(X_test)
            score_metric = "R² Variance Score"
            score_value = round(r2_score(y_test, predictions), 4)
            error_value = round(mean_absolute_error(y_test, predictions), 2)
            y_test_orig = y_test
            pred_orig = predictions

        preview_df = pd.DataFrame({"Actual Value": y_test_orig, "Model Prediction": pred_orig}).reset_index(drop=True)
        feat_imp_df = pd.DataFrame({"Feature Vector": feature_cols, "Significance Weight": model.feature_importances_}).sort_values(by="Significance Weight", ascending=False)
        
        return {
            "task_type": task_type,
            "score_metric": score_metric,
            "score_value": score_value,
            "error_value": error_value,
            "feature_importance": feat_imp_df,
            "preview_df": preview_df,
            "model_object": model,
            "encoders": encoders,
            "feature_cols": feature_cols,
            "target_col": target_col
        }

    @staticmethod
    def evaluate_available_features(df: pd.DataFrame) -> dict:
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        text_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        has_date = False
        for col in df.columns:
            if any(k in col.lower() for k in ['date', 'time', 'month', 'year']):
                has_date = True
                break
            try:
                if isinstance(df[col].dropna().iloc[0], str):
                    pd.to_datetime(df[col].dropna().iloc[0], errors='raise')
                    has_date = True
                    break
            except:
                continue
        return {
            "impute": df.isnull().sum().sum() > 0,
            "merge": len(text_cols) > 0 and len(num_cols) > 0,
            "anomaly": len(num_cols) > 0,
            "pivot": len(df.columns) >= 2 and len(num_cols) > 0,
            "search": not df.empty,
            "profile": True,
            "text": len(text_cols) > 0,
            "forecast": has_date and len(num_cols) > 0,
            "ml_studio": len(df.columns) >= 2
        }