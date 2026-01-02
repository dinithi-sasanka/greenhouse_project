# ============================
# 1. Important Libraries
# ============================
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import matplotlib.pyplot as plt

# ============================
# 2. Load Dataset
# ============================
df = pd.read_csv('data/dataset.csv', quotechar='"', skipinitialspace=True)
print("Dataset Loaded. Shape:", df.shape)
print(df.head())

# ============================
# 3. Check Missing Values
# ============================
print("\n--- Missing Values ---")
missing_counts = df.isnull().sum()
missing_percentage = df.isnull().mean() * 100
print(pd.DataFrame({'Missing Count': missing_counts, 'Missing %': missing_percentage}))

# Fill missing values
df['Prev_Harvest_kg'].fillna(df['Total_QTY_kg'].mean(), inplace=True)
df['Prev_price'].fillna(df['Avg_Price_Rs_per_kg'].mean(), inplace=True)

# ============================
# 4. Categorical Data Handling
# ============================
# Convert categorical column 'Holiday' to numeric (0/1)
if 'Holiday' in df.columns:
    df['Holiday'] = df['Holiday'].map({'Yes': 1, 'No': 0})

# ============================
# 5. EDA / Outlier Handling (Placeholder)
# ============================
# Example: check boxplot for harvest
plt.boxplot(df['Total_QTY_kg'])
plt.title("Harvest Quantity Distribution")
plt.show()

# You can add more plots, correlations, etc.

# ============================
# 6. Feature Engineering
# ============================
# Convert Month to datetime and numeric
df['Month_dt'] = pd.to_datetime(df['Month'])
df['Month_num'] = df['Month_dt'].map(lambda x: x.toordinal())
df['Month_only'] = df['Month_dt'].dt.month
df['Quarter'] = df['Month_dt'].dt.month.map(lambda m: (m-1)//3 + 1)

# Lag and moving average features for price
df['Price_Lag1'] = df['Avg_Price_Rs_per_kg'].shift(1).fillna(df['Avg_Price_Rs_per_kg'].mean())
df['Price_Lag2'] = df['Avg_Price_Rs_per_kg'].shift(2).fillna(df['Avg_Price_Rs_per_kg'].mean())
df['Price_MA3'] = df['Avg_Price_Rs_per_kg'].rolling(3, min_periods=1).mean()
df['Price_MA6'] = df['Avg_Price_Rs_per_kg'].rolling(6, min_periods=1).mean()

# ============================
# 7. Split Features & Labels
# ============================
harvest_features = ['Month_num', 'Temperature_C', 'Rainfall_mm', 'Prev_Harvest_kg', 
                    'Fertilizer_kg', 'Demand_Index', 'Supply_Index', 'Holiday']
X_harvest = df[harvest_features]
y_harvest = df['Total_QTY_kg']

price_features = harvest_features + ['Prev_price', 'Price_Lag1', 'Price_Lag2', 
                                     'Price_MA3', 'Price_MA6', 'Month_only', 'Quarter']
X_price = df[price_features]
y_price = df['Avg_Price_Rs_per_kg']

# ============================
# 8. Train/Test Split
# ============================
X_train_h, X_test_h, y_train_h, y_test_h = train_test_split(X_harvest, y_harvest, test_size=0.2, random_state=42)
X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(X_price, y_price, test_size=0.2, random_state=42)

# ============================
# 9. Feature Scaling
# ============================
harvest_scaler = StandardScaler()
X_train_h_scaled = harvest_scaler.fit_transform(X_train_h)
X_test_h_scaled = harvest_scaler.transform(X_test_h)

price_scaler = StandardScaler()
X_train_p_scaled = price_scaler.fit_transform(X_train_p)
X_test_p_scaled = price_scaler.transform(X_test_p)

# ============================
# 10. Train Random Forest Models
# ============================
harvest_model = RandomForestRegressor(n_estimators=200, random_state=42)
harvest_model.fit(X_train_h_scaled, y_train_h)

price_model = RandomForestRegressor(n_estimators=200, random_state=42)
price_model.fit(X_train_p_scaled, y_train_p)

# ============================
# 11. Save Models & Scalers
# ============================
joblib.dump(harvest_model, 'models/harvest_model.pkl')
joblib.dump(price_model, 'models/price_model.pkl')
joblib.dump(harvest_scaler, 'models/harvest_scaler.pkl')
joblib.dump(price_scaler, 'models/price_scaler.pkl')
print("\nModels & Scalers Saved Successfully")

# ============================
# 12. HARVEST MODEL METRICS
# ============================
harvest_pred_train = harvest_model.predict(X_train_h_scaled)
harvest_pred_test = harvest_model.predict(X_test_h_scaled)

print("\n========== HARVEST MODEL ==========")
print("Train RMSE :", np.sqrt(mean_squared_error(y_train_h, harvest_pred_train)))
print("Test RMSE  :", np.sqrt(mean_squared_error(y_test_h, harvest_pred_test)))
print("MAE        :", mean_absolute_error(y_test_h, harvest_pred_test))
print("R2 Score   :", r2_score(y_test_h, harvest_pred_test))

# ============================
# 13. PRICE MODEL METRICS
# ============================
price_pred_train = price_model.predict(X_train_p_scaled)
price_pred_test = price_model.predict(X_test_p_scaled)

print("\n========== PRICE MODEL ==========")
print("Train RMSE :", np.sqrt(mean_squared_error(y_train_p, price_pred_train)))
print("Test RMSE  :", np.sqrt(mean_squared_error(y_test_p, price_pred_test)))
print("MAE        :", mean_absolute_error(y_test_p, price_pred_test))
print("R2 Score   :", r2_score(y_test_p, price_pred_test))


harvest_acc = (1 - np.sqrt(mean_squared_error(y_test_h, harvest_pred_test)) / y_test_h.mean()) * 100
price_acc   = (1 - np.sqrt(mean_squared_error(y_test_p, price_pred_test)) / y_test_p.mean()) * 100

print(f"Harvest Accuracy: {harvest_acc:.2f}%")
print(f"Price Accuracy  : {price_acc:.2f}%")