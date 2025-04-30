from flask import Flask, render_template, request, jsonify

from ai.inference import predict_fraud, CATEGORIES

AMOUNT_WARNING_THRESHOLD = 5000


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        """Serve the main page."""
        return render_template("index.html", categories=CATEGORIES, amount_threshold=AMOUNT_WARNING_THRESHOLD)

    @app.route("/predict", methods=["POST"])
    def predict():
        """Handle prediction requests."""
        try:
            amount = float(request.form.get("amount"))
            category = request.form.get("category")
            hour = int(request.form.get("hour"))
            model_type = request.form.get("model_type", "knn")

            if amount <= 0:
                return jsonify({"error": "Amount must be positive"})

            if category not in CATEGORIES:
                return jsonify({"error": f"Invalid category. Must be one of: {', '.join(CATEGORIES)}"})

            if not (0 <= hour <= 23):
                return jsonify({"error": "Hour must be between 0 and 23"})

            if model_type.lower() not in ["knn", "decision_tree"]:
                return jsonify({"error": "Model type must be 'knn' or 'decision_tree'"})

            result = predict_fraud(amount, category, hour, model_type)
            return jsonify(result)

        except ValueError as e:
            return jsonify({"error": str(e)})
        except Exception as e:
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"})

    return app
