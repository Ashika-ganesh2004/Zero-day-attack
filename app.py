from flask import Flask, jsonify, request, session
from flask_cors import CORS
import random
import datetime

app = Flask(__name__)
app.secret_key = "super_secret_key"
CORS(app, supports_credentials=True)

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
# PUBLIC SIDEBAR APIs
# =====================================================

# -------- DASHBOARD --------
@app.route("/api/dashboard")
def dashboard():
    return jsonify({
        "total_traffic": random.randint(1000, 5000),
        "attacks_detected": random.randint(50, 200),
        "risk_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
        "model_status": admin_settings["model_status"]
    })


# -------- LIVE TRAFFIC --------
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


# -------- ATTACK LOGS --------
@app.route("/api/attack-logs")
def attack_logs():
    logs = [
        {
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "source_ip": f"10.0.0.{random.randint(1,255)}",
            "type": random.choice(["DDoS", "Port Scan", "Malware"]),
            "severity": random.choice(["LOW", "MEDIUM", "HIGH"])
        }
        for _ in range(8)
    ]
    return jsonify(logs)


# -------- THREAT ANALYSIS --------
@app.route("/api/threat-analysis")
def threat_analysis():
    normal = random.randint(80, 150)
    suspicious = random.randint(20, 60)
    malicious = random.randint(5, 40)

    if malicious > 25:
        level = "HIGH"
    elif malicious > 15:
        level = "MEDIUM"
    else:
        level = "LOW"

    return jsonify({
        "total_requests": normal + suspicious + malicious,
        "normal": normal,
        "suspicious": suspicious,
        "malicious": malicious,
        "threat_level": level
    })


# -------- RISK ASSESSMENT --------
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


# -------- MODEL STATUS --------
@app.route("/api/model-status")
def model_status():
    return jsonify({
        "model_name": "Zero-Day Detection Model",
        "accuracy": round(random.uniform(90, 98), 2),
        "f1_score": round(random.uniform(88, 96), 2),
        "status": admin_settings["model_status"],
        "last_trained": "2026-01-28"
    })


# -------- MODEL EXPLAINABILITY --------
@app.route("/api/model-explainability")
def model_explainability():
    features = {
        "Packet Size": random.randint(15, 30),
        "IP Reputation": random.randint(10, 25),
        "Protocol Type": random.randint(10, 20),
        "Connection Rate": random.randint(10, 25),
        "Time Behavior": random.randint(5, 20)
    }

    total = sum(features.values())
    importance = {k: round((v / total) * 100, 1) for k, v in features.items()}

    return jsonify({
        "prediction": random.choice(["Normal", "Attack"]),
        "risk_score": random.randint(60, 95),
        "confidence": random.randint(85, 98),
        "feature_importance": importance
    })


# -------- ALERTS --------
@app.route("/api/alerts")
def alerts():
    alerts_list = [
        {
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "ip": f"172.16.0.{random.randint(1,255)}",
            "severity": random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"]),
            "risk_score": random.randint(30, 95)
        }
        for _ in range(6)
    ]
    return jsonify(alerts_list)


# -------- REPORTS --------
@app.route("/api/reports")
def reports():
    return jsonify({
        "daily_attacks": random.randint(50, 200),
        "weekly_attacks": random.randint(300, 1000),
        "blocked_ips": random.randint(20, 100)
    })


# -------- SYSTEM HEALTH --------
@app.route("/api/system-health")
def system_health():
    return jsonify({
        "cpu_usage": random.randint(20, 80),
        "memory_usage": random.randint(30, 90),
        "disk_usage": random.randint(40, 85),
        "status": "HEALTHY"
    })


# =====================================================
# ADMIN AUTHENTICATION (PROTECTED ROUTES)
# =====================================================

@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json()
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


@app.route("/api/admin/settings")
def get_settings():
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(admin_settings)


@app.route("/api/admin/update-threshold", methods=["POST"])
def update_threshold():
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    admin_settings["normal_threshold"] = float(data.get("normal_threshold", 0.6))
    admin_settings["suspicious_threshold"] = float(data.get("suspicious_threshold", 0.8))

    return jsonify({"message": "Thresholds updated successfully"})


@app.route("/api/admin/update-model", methods=["POST"])
def update_model():
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    admin_settings["model_status"] = data.get("status", "ACTIVE")

    return jsonify({"message": "Model updated successfully"})


@app.route("/api/admin/users", methods=["POST"])
def add_user():
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    admin_settings["users"].append({
        "username": data.get("username"),
        "role": data.get("role")
    })

    return jsonify({"users": admin_settings["users"]})


@app.route("/api/admin/users/<username>", methods=["DELETE"])
def delete_user(username):
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 401

    admin_settings["users"] = [
        user for user in admin_settings["users"]
        if user["username"] != username
    ]

    return jsonify({"users": admin_settings["users"]})


# =====================================================
# RUN
# =====================================================

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)