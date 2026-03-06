import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from statsmodels.tsa.arima.model import ARIMA

def Wykonaj_Prognozę(method: str, X,y):


    # --- 1. REGRESJA LINIOWA ---
    if method == "LinearRegression":
        model = LinearRegression()
        model.fit(X, y)
        return float(model.predict([[len(y)]])[0])

    # --- 2. RANDOM FOREST ---
    elif method == "RandomForest":
        model = RandomForestRegressor(n_estimators=300, random_state=42)
        model.fit(X, y)
        return float(model.predict([[len(y)]])[0])

    # --- 3. POLYNOMIAL TREND (np. stopień 3) ---
    elif method == "Polynomial":
        model = make_pipeline(PolynomialFeatures(3), LinearRegression())
        model.fit(X, y)
        return float(model.predict([[len(y)]])[0])

    # --- 4. ARIMA ---
    elif method == "ARIMA":
        model = ARIMA(y, order=(1, 1, 1))
        model_fit = model.fit()
        return float(model_fit.forecast(steps=1)[0])

    else:
        raise ValueError("Nieznana metoda. Użyj: regresja, random_forest, polynomial, arima.")
