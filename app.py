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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model.pkl")

try:
    model = joblib.load(model_path)
except:
    model = None

# =====================================================
# HOME ROUTE (SHOW UI)
# =====================================================

@app.route("/")
def home():
    return render_template("index.html")

# =====================================================
# MOCK DATABASE
# =====================================================

ADMIN_USERS = {
    "admin": "admin123"
}

admin_settings = {
    "normal_threshold": 0.6,
    "suspicious_threshold": 0.8,
    "model_status": "ACTIVE",
    "users": [
        {"username": "admin", "role": "admin"},
        {"username": "analyst", "role": "user"}
    ]
}

# =====================================================
# HELPER FUNCTION
# =====================================================

def is_admin():
    return "admin" in session

# =====================================================
# PUBLIC APIs
# =====================================================

@app.route("/api/dashboard")
def dashboard():
    return jsonify({
        "total_traffic": random.randint(1000, 5000),
        "attacks_detected": random.randint(50, 200),
        "risk_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
        "model_status": admin_settings["model_status"]
    })


@app.route("/api/live-traffic")
def live_traffic():
    traffic = [
        {
            "ip": f"192.168.1.{random.randint(1,255)}",
            "packets": random.randint(10, 500),
            "protocol": random.choice(["TCP", "UDP", "ICMP"]),
            "status": random.choice(["Normal", "Suspicious", "Malicious"])
        }
        for _ in range(10)
    ]
    return jsonify(traffic)


@app.route("/api/risk-assessment")
def risk_assessment():
    score = random.randint(10, 95)

    if score > 70:
        level = "HIGH"
    elif score > 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return jsonify({
        "risk_score": score,
        "risk_level": level,
        "confidence": random.randint(80, 98)
    })

# =====================================================
# ADMIN ROUTES
# =====================================================

@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json()

    if not data:
        return jsonify({"success": False}), 400

    username = data.get("username")
    password = data.get("password")

    if username in ADMIN_USERS and ADMIN_USERS[username] == password:
        session["admin"] = username
        return jsonify({"success": True})

    return jsonify({"success": False}), 401


@app.route("/api/admin/check")
def admin_check():
    return jsonify({"logged_in": is_admin()})


@app.route("/api/admin/logout", methods=["POST"])
def admin_logout():
    session.pop("admin", None)
    return jsonify({"success": True})


# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
