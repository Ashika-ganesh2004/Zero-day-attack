from flask import Flask, jsonify, request, session, render_template
import random
import datetime
import os
import joblib

# =====================================================
# APP SETUP
# =====================================================

app = Flask(__name__)
app.secret_key = "super_secret_key"

# =====================================================
# LOAD MODEL (SAFE)
# =====================================================

model = None

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(BASE_DIR, "model.pkl")

    if os.path.exists(model_path):
        model = joblib.load(model_path)
        print("✅ Model loaded")
    else:
        print("⚠️ model.pkl not found")

except Exception as e:
    print("❌ Model error:", str(e))

# =====================================================
# HOME ROUTE (UI)
# =====================================================

@app.route("/")
def home():
    return render_template("index.html")

# =====================================================
# PUBLIC APIs
# =====================================================

@app.route("/api/dashboard")
def dashboard():
    return jsonify({
        "total_traffic": random.randint(1000, 5000),
        "attacks_detected": random.randint(50, 200),
        "risk_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
        "model_status": "ACTIVE"
    })

@app.route("/api/live-traffic")
def live_traffic():
    data = [
        {
            "ip": f"192.168.1.{random.randint(1,255)}",
            "packets": random.randint(10, 500),
            "status": random.choice(["Normal", "Suspicious", "Malicious"])
        }
        for _ in range(10)
    ]
    return jsonify(data)

@app.route("/api/risk-assessment")
def risk():
    score = random.randint(10, 95)
    return jsonify({
        "risk_score": score,
        "level": "HIGH" if score > 70 else "MEDIUM" if score > 40 else "LOW"
    })

# =====================================================
# PREDICTION API
# =====================================================

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        features = data.get("features")

        # Convert input string → list
        features = [float(x) for x in features.split(",")]

        # Dummy prediction (safe)
        prediction = random.choice(["Normal", "Attack"])
        risk_score = random.randint(50, 95)

        explanation = [
            {"feature": f"Feature {i+1}", "importance": random.random()}
            for i in range(5)
        ]

        return jsonify({
            "prediction": prediction,
            "risk_score": risk_score,
            "explanation": explanation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =====================================================
# ADMIN (OPTIONAL)
# =====================================================

@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json()

    if not data:
        return jsonify({"success": False}), 400

    if data.get("username") == "admin" and data.get("password") == "admin123":
        session["admin"] = "admin"
        return jsonify({"success": True})

    return jsonify({"success": False}), 401

# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
