

import pandas as pd
from dateutil.relativedelta import relativedelta
from utils.model_loader import (
    harvest_model,
    price_model,
    harvest_scaler,
    price_scaler
)
from datetime import datetime

DATA_PATH = "data/dataset.csv"
df_data = pd.read_csv(DATA_PATH)
df_data["Month_dt"] = pd.to_datetime(df_data["Month"])
df_data["Month_only"] = df_data["Month_dt"].dt.month

# Auto Future Prediction (12 months)


def predict_next_months(n_months=12):
    last_row = df_data.iloc[-1]
    prev_harvest = last_row["Total_QTY_kg"]
    prev_price = last_row["Avg_Price_Rs_per_kg"]

    # Start from current month instead of last row's month
    current_date = datetime.now()
    future_dates = [current_date + relativedelta(months=i) for i in range(n_months)]

    results = []

    seasonal_avg = df_data.groupby("Month_only")[[
        "Temperature_C","Rainfall_mm","Fertilizer_kg","Demand_Index","Supply_Index"
    ]].mean()

    for d in future_dates:
        month = d.month
        quarter = (month - 1)//3 + 1
        season = seasonal_avg.loc[month]

        harvest_row = {
            "Month_num": d.toordinal(),
            "Temperature_C": season["Temperature_C"],
            "Rainfall_mm": season["Rainfall_mm"],
            "Prev_Harvest_kg": prev_harvest,
            "Fertilizer_kg": season["Fertilizer_kg"],
            "Demand_Index": season["Demand_Index"],
            "Supply_Index": season["Supply_Index"],
            "Holiday": 0
        }

        X_h = harvest_scaler.transform(pd.DataFrame([harvest_row]))
        harvest_pred = harvest_model.predict(X_h)[0]

        price_row = {
            "Month_num": d.toordinal(),
            "Temperature_C": season["Temperature_C"],
            "Rainfall_mm": season["Rainfall_mm"],
            "Prev_Harvest_kg": harvest_pred,
            "Fertilizer_kg": season["Fertilizer_kg"],
            "Demand_Index": season["Demand_Index"],
            "Supply_Index": season["Supply_Index"],
            "Holiday": 0,
            "Prev_price": prev_price,
            "Price_Lag1": prev_price,
            "Price_Lag2": prev_price,
            "Price_MA3": prev_price,
            "Price_MA6": prev_price,
            "Month_only": month,
            "Quarter": quarter
        }

        X_p = price_scaler.transform(pd.DataFrame([price_row]))
        price_pred = price_model.predict(X_p)[0]

        results.append({
            "Month": d.strftime("%Y-%m"),
            "Harvest (kg)": round(harvest_pred,2),
            "Price (Rs/kg)": round(price_pred,2)
        })

        prev_harvest = harvest_pred
        prev_price = price_pred

    return pd.DataFrame(results)


# Manual Next-Month Prediction
def predict_manual_next_month(
    Temperature_C,
    Rainfall_mm,
    Fertilizer_kg,
    Demand_Index,
    Supply_Index,
    Holiday
):
    last_row = df_data.iloc[-1]
    prev_harvest = last_row["Total_QTY_kg"]
    prev_price = last_row["Avg_Price_Rs_per_kg"]

    d = pd.to_datetime(last_row["Month"]) + relativedelta(months=1)
    month = d.month
    quarter = (month-1)//3 + 1

    row = {
        "Month_num": d.toordinal(),
        "Temperature_C": Temperature_C,
        "Rainfall_mm": Rainfall_mm,
        "Prev_Harvest_kg": prev_harvest,
        "Fertilizer_kg": Fertilizer_kg,
        "Demand_Index": Demand_Index,
        "Supply_Index": Supply_Index,
        "Holiday": Holiday,
        "Prev_price": prev_price,
        "Price_Lag1": prev_price,
        "Price_Lag2": prev_price,
        "Price_MA3": prev_price,
        "Price_MA6": prev_price,
        "Month_only": month,
        "Quarter": quarter
    }

    harvest_features = ["Month_num","Temperature_C","Rainfall_mm",
                        "Prev_Harvest_kg","Fertilizer_kg",
                        "Demand_Index","Supply_Index","Holiday"]

    price_features = harvest_features + ["Prev_price","Price_Lag1","Price_Lag2",
                                         "Price_MA3","Price_MA6","Month_only","Quarter"]

    X_h = harvest_scaler.transform(pd.DataFrame([row])[harvest_features])
    harvest_pred = harvest_model.predict(X_h)[0]

    row["Prev_Harvest_kg"] = harvest_pred

    X_p = price_scaler.transform(pd.DataFrame([row])[price_features])
    price_pred = price_model.predict(X_p)[0]

    return pd.DataFrame([{
        "Month": d.strftime("%Y-%m"),
        "Harvest (kg)": round(harvest_pred,2),
        "Price (Rs/kg)": round(price_pred,2)
    }])
