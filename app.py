from flask import Flask, render_template, request, redirect, url_for, flash

# ML functions
from utils.preprocess import predict_next_months, predict_manual_next_month

# DB functions
from utils.db import (
    fetch_users,
    add_user,
    delete_user,
    update_user,
    search_users
)

app = Flask(__name__)
app.secret_key = "supersecretkey"  # for flash messages

# ----------------------
# HOME
# ----------------------
@app.route('/')
def home():
    return redirect(url_for('dashboard'))

# ----------------------
# DASHBOARD (AUTO ONLY)
# ----------------------
@app.route('/dashboard')
def dashboard():
    auto_predictions = predict_next_months().to_dict(orient='records')
    return render_template('dashboard.html', auto_predictions=auto_predictions)

# ----------------------
# NEXT MONTH PREDICTION
# ----------------------
@app.route('/next-month-prediction', methods=['GET', 'POST'])
def next_month_prediction():
    manual_predictions = None
    if request.method == 'POST':
        manual_predictions = predict_manual_next_month(
            Temperature_C=float(request.form['Temperature_C']),
            Rainfall_mm=float(request.form['Rainfall_mm']),
            Fertilizer_kg=float(request.form['Fertilizer_kg']),
            Demand_Index=float(request.form['Demand_Index']),
            Supply_Index=float(request.form['Supply_Index']),
            Holiday=int(request.form['Holiday'])
        ).to_dict(orient='records')
    return render_template('next_month_prediction.html', manual_predictions=manual_predictions)

# ----------------------
# USERS (VIEW + ADD + SEARCH)
# ----------------------
@app.route('/users', methods=['GET', 'POST'])
def users():
    search = request.args.get('search')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        email = request.form['email']
        address = request.form['address']
        telephone = request.form['telephone']

        # Basic server-side validation
        if len(username) < 3 or len(password) < 6 or not email or not address or not telephone.isdigit() or len(telephone) != 10:
            flash("Invalid input! Check all fields.")
        else:
            add_user(username, password, role, email, address, telephone)
            flash("User added successfully!")
        return redirect(url_for('users'))

    if search:
        users_list = search_users(search)
    else:
        users_list = fetch_users()

    return render_template('users.html', users=users_list)

# ----------------------
# UPDATE USER
# ----------------------
@app.route('/edit_user/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    username = request.form['username']
    role = request.form['role']
    email = request.form['email']
    address = request.form['address']
    telephone = request.form['telephone']

    # Server-side validation
    if len(username) < 3 or not email or not address or not telephone.isdigit() or len(telephone) != 10:
        flash("Invalid input! Cannot update user.")
    else:
        update_user(user_id, username, role, email, address, telephone)
        flash("User updated successfully!")
    return redirect(url_for('users'))

# ----------------------
# DELETE USER
# ----------------------
@app.route('/delete_user/<int:user_id>')
def delete_user_route(user_id):
    delete_user(user_id)
    flash("User deleted successfully!")
    return redirect(url_for('users'))

# ----------------------
# LOGOUT
# ----------------------
@app.route('/logout')
def logout():
    return redirect(url_for('dashboard'))

# ----------------------
# RUN APP
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)
