from flask import Flask, render_template, request, redirect, url_for
from utils.preprocess import predict_next_months, predict_manual_next_month
from utils.db import fetch_users

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    auto_predictions = predict_next_months().to_dict(orient='records')
    return render_template('dashboard.html', auto_predictions=auto_predictions)

# -------------------- Manual Next-Month Prediction --------------------
@app.route('/next-month-prediction', methods=['GET','POST'])
def next_month_prediction():
    manual_predictions = None
    if request.method == 'POST':
        temp = float(request.form['Temperature_C'])
        rain = float(request.form['Rainfall_mm'])
        fert = float(request.form['Fertilizer_kg'])
        demand = float(request.form['Demand_Index'])
        supply = float(request.form['Supply_Index'])
        holiday = int(request.form['Holiday'])

        manual_predictions = predict_manual_next_month(
            Temperature_C=temp,
            Rainfall_mm=rain,
            Fertilizer_kg=fert,
            Demand_Index=demand,
            Supply_Index=supply,
            Holiday=holiday
        ).to_dict(orient='records')

    return render_template('next_month_prediction.html', manual_predictions=manual_predictions)

@app.route('/users')
def users():
    users_list = fetch_users()
    return render_template('users.html', users=users_list)

@app.route('/logout')
def logout():
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(debug=True)
