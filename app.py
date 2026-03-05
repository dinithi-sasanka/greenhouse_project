from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps


from utils.preprocess import predict_next_months, predict_manual_next_month


from utils.db import (
    fetch_users, add_user, delete_user, update_user, search_users,
    validate_user, fetch_user_by_username, update_user_password
)

app = Flask(__name__)
import os
app.secret_key = os.environ.get("SECRET_KEY")


# -------------------------------
# DECORATORS
# -------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Access denied! Admins only.", "error")
            return redirect(url_for('users'))
        return f(*args, **kwargs)
    return decorated_function

# -------------------------------
# DEFAULT ROUTE
# -------------------------------
@app.route('/')
def index():
    return redirect(url_for('login'))

# -------------------------------
# LOGIN
# -------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = validate_user(username, password)
        if user:
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f"Welcome, {user['username']}!")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password!", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

# -------------------------------
# FORGOT PASSWORD
# -------------------------------
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        user = fetch_user_by_username(username)

        if not user:
            flash("Username not found.", "error")
            return redirect(url_for('forgot_password'))

        return redirect(url_for('reset_password', username=username))

    return render_template('forgot_password.html')


@app.route('/reset-password/<username>', methods=['GET', 'POST'])
def reset_password(username):
    if request.method == 'POST':
        new_password = request.form['new_password']
        update_user_password(username, new_password)
        flash("Password updated successfully! You can now login.")
        return redirect(url_for('login'))

    return render_template('reset_password.html', username=username)

# -------------------------------
# LOGOUT
# -------------------------------
@app.route('/logout')
@login_required
def logout():
    return """
        <script>
            if(confirm('Do you want to logout from the system?')) {
                window.location.href='/logout_confirm';
            } else {
                window.location.href='/dashboard';
            }
        </script>
    """

@app.route('/logout_confirm')
@login_required
def logout_confirm():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for('login'))

# -------------------------------
# DASHBOARD
# -------------------------------
@app.route('/dashboard')
@login_required
def dashboard():
    auto_predictions = predict_next_months().to_dict(orient='records')
    return render_template('dashboard.html', auto_predictions=auto_predictions)

# -------------------------------
# NEXT MONTH PREDICTION
# -------------------------------
@app.route('/next-month-prediction', methods=['GET', 'POST'])
@login_required
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

    return render_template(
        'next_month_prediction.html',
        manual_predictions=manual_predictions
    )

# -------------------------------
# USERS PAGE
# -------------------------------
@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    search = request.args.get('search')

    # ADD USER (admin only)
    if request.method == 'POST' and session.get('role') == 'admin':
        add_user(
            request.form['username'],
            request.form['password'],
            request.form['role'],
            request.form['email'],
            request.form['address'],
            request.form['telephone']
        )
        flash("User added successfully!")
        return redirect(url_for('users'))

    # SEARCH USERS
    if search:
        users_list = search_users(search)
    else:
        users_list = fetch_users()

    return render_template(
        'users.html',
        users=users_list,
        role=session.get('role')
    )

# -------------------------------
# EDIT USER (admin only)
# -------------------------------
@app.route('/edit_user/<user_id>', methods=['POST'])
@login_required
@admin_required
def edit_user(user_id):
    new_password = request.form.get('password')  # optional

    update_user(
        user_id,
        request.form['username'],
        request.form['role'],
        request.form['email'],
        request.form['address'],
        request.form['telephone'],
        password=new_password if new_password else None
    )

    flash("User updated successfully!")
    return redirect(url_for('users'))

# -------------------------------
# DELETE USER (admin only)
# -------------------------------
@app.route('/delete_user/<user_id>')
@login_required
@admin_required
def delete_user_route(user_id):
    delete_user(user_id)
    flash("User deleted successfully!")
    return redirect(url_for('users'))

# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
