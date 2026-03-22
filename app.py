# =====================================================
# PREDICTION API (FIXED)
# =====================================================

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data or "features" not in data:
            return jsonify({"error": "No input provided"}), 400

        raw = data.get("features")

        # ✅ safer conversion (handles spaces)
        features = [float(x.strip()) for x in raw.split(",") if x.strip() != ""]

        if len(features) == 0:
            return jsonify({"error": "Empty input"}), 400

        # Dummy prediction
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
