# ============================
# STEP 1: Import Libraries
# ============================

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# ============================
# STEP 2: Load Dataset
# ============================

DATA_PATH = "data/dataset.csv"  # <- put your CSV here
df = pd.read_csv(DATA_PATH, quotechar='"', skipinitialspace=True)
print("Dataset Loaded. Shape:", df.shape)
df.head()

# ============================
# STEP 3: Inspect Dataset
# ============================

df.info()
df.describe()

# ============================
# STEP 4: Check Missing Values
# ============================

missing_counts = df.isnull().sum()
missing_percentage = df.isnull().mean() * 100
print(pd.DataFrame({'Missing Count': missing_counts, 'Missing %': missing_percentage}))

# ============================
# STEP 5: Fill Missing Values
# ============================

numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

if 'Holiday' in df.columns:
    df['Holiday'] = df['Holiday'].map({'Yes': 1, 'No': 0}).fillna(0)

# ============================
# STEP 6: Exploratory Data Analysis (EDA)
# ============================

plt.figure(figsize=(8,5))
sns.boxplot(y=df['Total_QTY_kg'])
plt.title("Harvest Quantity Distribution")
plt.show()

plt.figure(figsize=(8,5))
sns.histplot(df['Avg_Price_Rs_per_kg'], bins=20, kde=True)
plt.title("Average Price Distribution")
plt.show()

df['Month_dt'] = pd.to_datetime(df['Month'])
df['Month_num'] = df['Month_dt'].map(lambda x: x.toordinal())
numeric_df = df.select_dtypes(include=[np.number])
plt.figure(figsize=(12,8))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.show()

# ============================
# STEP 7: Feature Engineering
# ============================

df['Month_only'] = df['Month_dt'].dt.month
df['Quarter'] = df['Month_dt'].dt.month.map(lambda m: (m-1)//3 + 1)

# Lag and moving average features for price
df['Price_Lag1'] = df['Avg_Price_Rs_per_kg'].shift(1).fillna(df['Avg_Price_Rs_per_kg'].mean())
df['Price_Lag2'] = df['Avg_Price_Rs_per_kg'].shift(2).fillna(df['Avg_Price_Rs_per_kg'].mean())
df['Price_MA3'] = df['Avg_Price_Rs_per_kg'].rolling(3, min_periods=1).mean()
df['Price_MA6'] = df['Avg_Price_Rs_per_kg'].rolling(6, min_periods=1).mean()

# ============================
# STEP 8: Feature Selection
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
# STEP 9: Train/Test Split
# ============================

X_train_h, X_test_h, y_train_h, y_test_h = train_test_split(
    X_harvest, y_harvest, test_size=0.2, random_state=42
)
X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(
    X_price, y_price, test_size=0.2, random_state=42
)

# ============================
# STEP 10: Feature Scaling
# ============================

harvest_scaler = StandardScaler()
X_train_h_scaled = harvest_scaler.fit_transform(X_train_h)
X_test_h_scaled = harvest_scaler.transform(X_test_h)

price_scaler = StandardScaler()
X_train_p_scaled = price_scaler.fit_transform(X_train_p)
X_test_p_scaled = price_scaler.transform(X_test_p)

# ============================
# STEP 11: Model Training
# ============================

# Random Forest
harvest_rf = RandomForestRegressor(n_estimators=200, random_state=42)
harvest_rf.fit(X_train_h_scaled, y_train_h)

price_rf = RandomForestRegressor(n_estimators=200, random_state=42)
price_rf.fit(X_train_p_scaled, y_train_p)

# Gradient Boosting
harvest_gb = GradientBoostingRegressor(n_estimators=200, random_state=42)
harvest_gb.fit(X_train_h_scaled, y_train_h)

price_gb = GradientBoostingRegressor(n_estimators=200, random_state=42)
price_gb.fit(X_train_p_scaled, y_train_p)

# Linear / Ridge
harvest_lr = LinearRegression()
harvest_lr.fit(X_train_h_scaled, y_train_h)

price_ridge = Ridge(alpha=1.0)
price_ridge.fit(X_train_p_scaled, y_train_p)

# ============================
# STEP 12: Save Models & Scalers
# ============================

os.makedirs('models', exist_ok=True)

joblib.dump(harvest_rf, 'models/harvest_rf.pkl')
joblib.dump(harvest_gb, 'models/harvest_gb.pkl')
joblib.dump(price_rf, 'models/price_rf.pkl')
joblib.dump(price_gb, 'models/price_gb.pkl')
joblib.dump(harvest_lr, 'models/harvest_lr.pkl')
joblib.dump(price_ridge, 'models/price_ridge.pkl')
joblib.dump(harvest_scaler, 'models/harvest_scaler.pkl')
joblib.dump(price_scaler, 'models/price_scaler.pkl')

print("Models & Scalers Saved Successfully")

# ============================
# STEP 13: Model Evaluation
# ============================

def evaluate_model(y_true, y_pred, name="Model"):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    acc = (1 - rmse / y_true.mean()) * 100
    print(f"\n{name} Metrics:")
    print(f"RMSE : {rmse:.4f}")
    print(f"MAE  : {mae:.4f}")
    print(f"R2   : {r2:.4f}")
    print(f"Accuracy: {acc:.2f}%")
    return rmse, mae, r2, acc

# Harvest Models
print("\n========== HARVEST MODELS ==========")
evaluate_model(y_test_h, harvest_rf.predict(X_test_h_scaled), "Harvest RF")
evaluate_model(y_test_h, harvest_gb.predict(X_test_h_scaled), "Harvest GB")
evaluate_model(y_test_h, harvest_lr.predict(X_test_h_scaled), "Harvest LR")

# Price Models
print("\n========== PRICE MODELS ==========")
evaluate_model(y_test_p, price_rf.predict(X_test_p_scaled), "Price RF")
evaluate_model(y_test_p, price_gb.predict(X_test_p_scaled), "Price GB")
evaluate_model(y_test_p, price_ridge.predict(X_test_p_scaled), "Price Ridge")

# ============================
# STEP 14: Feature Importance Visualization
# ============================

feat_importances = pd.Series(harvest_rf.feature_importances_, index=harvest_features)
feat_importances.sort_values().plot(kind='barh', figsize=(8,5))
plt.title("Harvest Feature Importance (RF)")
plt.show()

feat_importances_price = pd.Series(price_rf.feature_importances_, index=price_features)
feat_importances_price.sort_values().plot(kind='barh', figsize=(8,5))
plt.title("Price Feature Importance (RF)")
plt.show()