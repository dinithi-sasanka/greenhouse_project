
---

# 🌱 AI-Powered Greenhouse Harvest and Price Prediction System

## 📌 Project Overview

This project presents an **AI-based decision support system for greenhouse agriculture**, developed as a case study for **Blue Water Farms (Pvt) Ltd, Sri Lanka**. The system predicts **future cucumber harvest quantities and market prices** using machine learning techniques.

The system integrates **machine learning models, a web-based dashboard, and secure user management** to help farm managers make data-driven decisions related to production planning and market strategies.

---

# 🎯 Objectives

The main objectives of this project are:

* Predict future **greenhouse cucumber harvest quantities**
* Forecast **market prices for cucumbers**
* Provide **automatic multi-month prediction**
* Allow **manual prediction simulation using environmental inputs**
* Provide **secure user authentication and role-based access**
* Visualize prediction results through **interactive dashboards**

---

# ⚙️ System Features

### 🔐 Authentication System

* Secure login system
* Password reset functionality
* Role-based access control

### 📊 Prediction Dashboard

* Displays **12-month future predictions**
* Interactive charts for harvest and price trends
* Tabular forecast results

### 🤖 AI Prediction Module

* Harvest prediction using environmental and operational variables
* Price prediction using historical price trends

### 🧪 Manual Prediction

Users can simulate next month predictions by entering:

* Temperature
* Rainfall
* Fertilizer usage
* Demand index
* Supply index
* Holiday indicator

### 👥 User Management

Admin users can:

* Add users
* Update users
* Delete users
* Search users

---

# 🧠 Machine Learning Models

Multiple machine learning models were evaluated:

### Harvest Prediction

* Random Forest Regressor
* Gradient Boosting Regressor
* Linear Regression

### Price Prediction

* Random Forest Regressor
* Gradient Boosting Regressor
* Ridge Regression

### Final Selected Models

| Prediction Type    | Model                       |
| ------------------ | --------------------------- |
| Harvest Prediction | Gradient Boosting Regressor |
| Price Prediction   | Ridge Regression            |

---

# 📊 Dataset

The dataset used for training the machine learning models contains **monthly greenhouse production and price records**.

**Data Source:**
Blue Water Farms (Pvt) Ltd internal farm management system.

**Data Period:**
January 2010 – December 2025

The dataset includes:

* Month
* Harvest quantity (kg)
* Average price (Rs/kg)
* Temperature
* Rainfall
* Fertilizer usage
* Previous harvest
* Demand index
* Supply index
* Holiday indicator
* Previous price

The data was obtained from **printed reports generated from the farm's internal system** and digitized into structured datasets for machine learning analysis.

---

# 🛠 Technology Stack

### Backend

* Python
* Flask

### Machine Learning

* Scikit-learn
* Pandas
* NumPy
* Joblib

### Database

* MongoDB Atlas

### Frontend

* HTML
* CSS
* Jinja2
* Chart.js

---

# 📁 Project Structure

```
greenhouse_project/
│
├── app.py
├── requirements.txt
├── hash_passwords.py
├── migrate_users.py
├── test_db.py
├── test_mongo.py
│
├── data/
│   └── dataset.csv
│
├── ml/
│   ├── train_model.py
│   └── models/
│       ├── harvest_gb.pkl
│       ├── harvest_lr.pkl
│       ├── harvest_rf.pkl
│       ├── harvest_scaler.pkl
│       ├── price_gb.pkl
│       ├── price_rf.pkl
│       ├── price_ridge.pkl
│       └── price_scaler.pkl
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── forgot_password.html
│   ├── reset_password.html
│   ├── dashboard.html
│   ├── next_month_prediction.html
│   └── users.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── charts.js
│   │
│   └── images/
│       └── logo.png
│
├── utils/
│   ├── db.py
│   ├── model_loader.py
│   └── preprocess.py
│
└── venv/
```
You can add a **Database Setup section** in your README or User Guide so others know how to configure MongoDB for your project.

Below is a clean **GitHub-ready section** you can paste.

---

# 🗄️ Database Setup (MongoDB Atlas)

![Image](https://images.contentstack.io/v3/assets/blt7151619cb9560896/blt2eb1cb5cbdff2c5e/690394c190b8c9bf0bec0d01/Final_Natural_Language_Query_Bar-1zdm6hqiyq.gif)



The system uses **MongoDB Atlas (Cloud NoSQL Database)** to store user account information and authentication data.

The database stores:

* User accounts
* Password hashes
* User roles (Admin / User)
* Contact information

---

# 📂 Database Structure

Database Name

```
greenhouse_db
```

Collection

```
users
```

Example Document

```json
{
  "_id": "ObjectId",
  "username": "dinithi",
  "password": "hashed_password",
  "role": "admin",
  "email": "example@gmail.com",
  "address": "Colombo, Sri Lanka",
  "telephone": "0712345678"
}
```

Passwords are securely stored using **Werkzeug password hashing**.

---

# ⚙️ MongoDB Atlas Setup

### 1️⃣ Create MongoDB Atlas Account

Go to:

<img width="975" height="493" alt="image" src="https://github.com/user-attachments/assets/1abc9c5e-4b51-4eb8-87e1-0b9b87bee4bb" />



Create a free account.

---

### 2️⃣ Create a Cluster

1. Click **Create Cluster**
2. Select **Free Tier (M0)**
3. Choose a cloud provider and region
4. Click **Create Cluster**

---

### 3️⃣ Create Database

After the cluster is ready:

1. Open **Database → Browse Collections**
2. Click **Create Database**

Database Name

```
greenhouse_db
```

Collection Name

```
users
```

---

### 4️⃣ Add Database User

Go to:

```
Database Access
```

Create a new database user with:

```
Username: your_username
Password: your_password
```

Give permission:

```
Read and Write to any database
```

---

### 5️⃣ Get Connection String

Go to:

```
Clusters → Connect → Drivers
```

Copy the connection string.

Example:

```
mongodb+srv://username:password@cluster.mongodb.net/greenhouse_db
```

---

### 6️⃣ Add Environment Variable

Create a `.env` file in the project root:

```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/greenhouse_db
```

Your Flask application reads this connection string to connect to MongoDB.

---

# 🔗 Database Connection (utils/db.py)

The application connects to MongoDB using **PyMongo**.

Example connection:

```python
from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client["greenhouse_db"]
users_collection = db["users"]
```

---

# 🔐 Security

The system implements the following security mechanisms:

* Password hashing using **Werkzeug**
* Role-based access control (Admin / User)
* Secure environment variables using `.env`

---


---

# 🚀 How to Run the Project

---

# 📦 Dependencies

The project requires the following Python libraries to run the web application and machine learning models.

```
Flask==3.1.2
Werkzeug==3.1.4
Jinja2==3.1.6
itsdangerous==2.2.0
click==8.3.1
blinker==1.9.0

pandas==2.3.3
numpy==2.3.5
scikit-learn==1.7.2
scipy==1.16.3
joblib==1.5.2
threadpoolctl==3.6.0

python-dateutil==2.9.0.post0
pytz==2025.2
tzdata==2025.2
six==1.17.0

python-dotenv==1.2.1
pymongo==4.10.1
```

---

# ⚙️ Installation

Follow these steps to set up the project environment.

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/greenhouse_project.git
cd greenhouse_project
```

### 2️⃣ Create a virtual environment

```
python -m venv venv
```

### 3️⃣ Activate the virtual environment

**Windows**

```
venv\Scripts\activate
```

**Mac/Linux**

```
source venv/bin/activate
```

### 4️⃣ Install required packages

```
pip install -r requirements.txt
```

---

# 🚀 Run the Application

```
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---



---

# 📘 User Guide

This section explains how to use the **AI-Powered Greenhouse Harvest and Price Prediction System** and navigate through its main features.

---

# 🔐 1. Login to the System

<img width="975" height="489" alt="image" src="https://github.com/user-attachments/assets/e17f2e3f-a5ab-4fd4-b89e-183ca7732d18" />


### Steps

1. Open the application in your browser

   ```
   http://127.0.0.1:5000
   ```

2. Enter your **Username**

3. Enter your **Password**

4. Click **Login**

5. If credentials are correct, the system will redirect to the **Dashboard**.

---

# 🔑 2. Forgot Password

<img width="975" height="489" alt="image" src="https://github.com/user-attachments/assets/a3c0df8b-4c1b-4547-a783-4655bd0c01a4" />


If a user forgets their password:

1. Click **Forgot Password**
2. Enter the **Username**
3. Click **Continue**
4. The system will redirect to the **Reset Password page**

---

# 🔐 3. Reset Password

<img width="934" height="471" alt="image" src="https://github.com/user-attachments/assets/92b463be-17b6-47e1-bb7e-d7583eb68190" />

### Steps

1. Enter **New Password**
2. Confirm the **New Password**
3. Click **Reset Password**
4. The system will update the password and return to the login page.

---

# 📊 4. Dashboard – Automatic Prediction

<img width="975" height="492" alt="image" src="https://github.com/user-attachments/assets/540d1026-1ae2-4d13-8dee-7e17b369794a" />

<img width="975" height="500" alt="image" src="https://github.com/user-attachments/assets/0433e445-8ff0-43e6-a05a-8c7108e431b4" />

After login, users will see the **Dashboard page**.

### Features

The dashboard displays:

* **12-month future harvest predictions**
* **12-month price predictions**
* Interactive **prediction charts**
* Prediction data in **table format**

This helps farm managers **plan production and pricing strategies**.

---

# 📈 5. Manual Next-Month Prediction

<img width="975" height="489" alt="image" src="https://github.com/user-attachments/assets/7e0c570f-7582-4d1a-b5a3-c578117b28c9" />

Users can manually simulate predictions for the next month.

### Input Variables

Users must enter:

* Temperature (°C)
* Rainfall (mm)
* Fertilizer usage (kg)
* Demand index
* Supply index
* Holiday indicator (0 or 1)

### Steps

1. Navigate to **Prediction**
2. Enter the required input values
3. Click **Predict Next Month**
4. The system displays predicted:

* Harvest quantity (kg)
* Market price (Rs/kg)

---

Good catch 👍 — you should clarify the **role permissions** in the User Guide.

Update the **User Management section** like this:

---

# 👥 6. User Management

The **Users page** allows administrators and normal users to view system users.

### 👑 Admin Permissions

Admin users can:

* Add new users
* Update existing user information
* Delete users
* Search users
* View all users

<img width="975" height="491" alt="image" src="https://github.com/user-attachments/assets/daa75fa7-93fc-4cd2-9c93-9c2a1ec64708" />
<img width="975" height="492" alt="image" src="https://github.com/user-attachments/assets/1386099e-3c7b-4623-a03c-431bcf23a91a" />


### 👤 Normal User Permissions

Normal users can only:

* View the user list
* Search users
<img width="975" height="471" alt="image" src="https://github.com/user-attachments/assets/cc37d2ef-5473-473a-8683-b636d0f20e57" />

Normal users **cannot add, update, or delete users**.

### ➕ Add New User (Admin Only)

Administrators can create new users by filling in the following fields:

* Username
* Password
* Role (Admin / User)
* Email
* Address
* Telephone

Then click **Add User**.

---



| Menu           | Description                                      |
| -------------- | ------------------------------------------------ |
| **Dashboard**  | Displays automatic harvest and price predictions |
| **Prediction** | Allows manual next-month prediction              |
| **Users**      | View users (Admin can add/update/delete)         |
| **Logout**     | Ends the current session                         |

---


# 🚪 Logout

To exit the system:

1. Click **Logout** in the navigation menu.
2. The system will terminate the session and return to the **Login page**.

---



# 🔮 Future Improvements

Future versions of this system can include:

* Support for **multiple crops**
* **Mobile application** for farmers
* Integration with **IoT greenhouse sensors**
* Real-time environmental monitoring
* Expansion for **farmers across Sri Lanka**

---

# 

This system was developed as part of a **final year undergraduate project** focusing on the application of **Artificial Intelligence in Agriculture**.

The system demonstrates how machine learning can be applied to **improve agricultural decision-making and forecasting**.

---

# 👨‍💻 Author

**Dinithi Sasanka**
**Email: dinithisasanka01@gmail.com**

Final Year Undergraduate
Software Engineering


