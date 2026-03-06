import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error

from statsmodels.tsa.arima.model import ARIMA


def najlepsza_prognoza(dates, values):

    df = pd.DataFrame({
        "date": pd.to_datetime(dates),
        "value": values
    })

    df = df.sort_values("date")

    # zamiana daty na liczbę
    df["t"] = (df["date"] - df["date"].min()).dt.days

    X = df[["t"]]
    y = df["value"]

    # podział train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, shuffle=False, test_size=0.2
    )

    results = {}

    # 1 regresja liniowa
    model_lr = LinearRegression()
    model_lr.fit(X_train, y_train)
    pred = model_lr.predict(X_test)
    results["LinearRegression"] = mean_absolute_error(y_test, pred)

    # 2 random forest
    model_rf = RandomForestRegressor(n_estimators=200)
    model_rf.fit(X_train, y_train)
    pred = model_rf.predict(X_test)
    results["RandomForest"] = mean_absolute_error(y_test, pred)

    # 3 polynomial trend
    model_poly = Pipeline([
        ("poly", PolynomialFeatures(degree=3)),
        ("lr", LinearRegression())
    ])

    model_poly.fit(X_train, y_train)
    pred = model_poly.predict(X_test)
    results["Polynomial"] = mean_absolute_error(y_test, pred)

    # 4 ARIMA
    arima = ARIMA(y_train, order=(2,1,2))
    arima_model = arima.fit()
    pred = arima_model.forecast(len(y_test))
    results["ARIMA"] = mean_absolute_error(y_test, pred)

    # wybór najlepszego modelu
    best = min(results, key=results.get)

    return  best
    # {
    #     "best_model": best,
    #     "scores": results
    #
    # }

