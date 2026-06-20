"""
data_analysis/predictive_models.py — Machine Learning Engine
============================================================
Provides predictive analytics capabilities using scikit-learn and xgboost.
Models are trained on-the-fly for exploratory purposes.
"""

from __future__ import annotations

import pandas as pd
import numpy as np

try:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import r2_score, mean_absolute_error
    import xgboost as xgb
except ImportError:
    pass

from src.visualization.chart_factory import VisualizationEngine
from src.feature_engineering.feature_store import FeatureEngineeringEngine
from src.core.logging_manager import get_logger

logger = get_logger("src.machine_learning.model_training")


class PredictiveEngine:
    """Trains and evaluates Machine Learning models for business predictions."""

    def __init__(self):
        self.mapping_engine = VisualizationEngine()
        self.feature_engine = FeatureEngineeringEngine()

    def train_sales_predictor(self, df: pd.DataFrame) -> dict | None:
        """
        Trains a Random Forest Regressor to predict Revenue based on available numerical columns.
        Returns evaluation metrics and feature importance.
        """
        try:
            mapping = self.mapping_engine.auto_map_columns(df)
            rev_col = mapping["revenue"]
            
            if not rev_col:
                return None
                
            # Select numerical features for regression
            numeric_df = df.select_dtypes(include=[np.number]).dropna()
            if numeric_df.empty or len(numeric_df) < 50:
                return {"error": "Not enough numerical data or rows (<50) to train a model."}
                
            # Prepare X and y
            y = numeric_df[rev_col]
            X = numeric_df.drop(columns=[rev_col])
            
            if X.empty:
                return {"error": "No independent numerical variables found to predict Revenue."}
                
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train Random Forest
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Evaluate
            predictions = model.predict(X_test)
            r2 = r2_score(y_test, predictions)
            mae = mean_absolute_error(y_test, predictions)
            
            # Feature Importance
            importance = pd.DataFrame({
                'Feature': X.columns,
                'Importance': model.feature_importances_
            }).sort_values('Importance', ascending=False).head(5)
            
            return {
                "status": "success",
                "model_type": "Random Forest Regressor",
                "r2_score": r2,
                "mae": mae,
                "feature_importance": importance,
                "dataset_size": len(numeric_df)
            }
            
        except Exception as e:
            logger.error(f"Sales Prediction Error: {e}")
            return {"error": str(e)}

    def train_churn_predictor(self, df: pd.DataFrame) -> dict | None:
        """
        Trains an XGBoost Classifier on engineered customer features to predict Churn.
        """
        try:
            # Generate Customer Features
            cust_features = self.feature_engine.engineer_customer_features(df)
            if cust_features is None or 'Churn_Indicator' not in cust_features.columns:
                return {"error": "Could not engineer customer features. Ensure Date and Customer columns exist."}
                
            # Drop identifiers and datetime
            X = cust_features.select_dtypes(include=[np.number]).drop(columns=['Churn_Indicator'])
            y = cust_features['Churn_Indicator']
            
            # Check class balance
            if len(y.unique()) < 2:
                return {"error": "Cannot train churn model: All customers belong to a single class (e.g. all active or all churned)."}
                
            if len(X) < 20:
                return {"error": "Not enough customer data to train."}
                
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
            
            # Train XGBoost
            model = xgb.XGBClassifier(eval_metric='logloss', use_label_encoder=False, random_state=42)
            model.fit(X_train, y_train)
            
            # Evaluate Accuracy
            accuracy = model.score(X_test, y_test)
            
            # Feature Importance
            importance = pd.DataFrame({
                'Feature': X.columns,
                'Importance': model.feature_importances_
            }).sort_values('Importance', ascending=False).head(5)
            
            return {
                "status": "success",
                "model_type": "XGBoost Classifier",
                "accuracy": accuracy,
                "feature_importance": importance,
                "customer_count": len(cust_features)
            }
            
        except Exception as e:
            logger.error(f"Churn Prediction Error: {e}")
            return {"error": str(e)}
