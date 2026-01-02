from flask import Flask, render_template, request
from utils.preprocess import predict_next_months, predict_manual_next_month

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def dashboard():
    auto_predictions = predict_next_months(12)  # Next 12 months
    manual_predictions = None

    if request.method == "POST":
        temp = float(request.form["Temperature_C"])
        rain = float(request.form["Rainfall_mm"])
        fert = float(request.form["Fertilizer_kg"])
        demand = float(request.form["Demand_Index"])
        supply = float(request.form["Supply_Index"])
        holiday = int(request.form["Holiday"])

        manual_predictions = predict_manual_next_month(temp, rain, fert, demand, supply, holiday)

    return render_template(
        "dashboard.html",
        auto_predictions=auto_predictions.to_dict(orient="records"),
        manual_predictions=manual_predictions.to_dict(orient="records") if manual_predictions is not None else None
    )

if __name__ == "__main__":
    app.run(debug=True)
