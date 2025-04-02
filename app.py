from flask import Flask, request, jsonify, render_template
import joblib
import logging
import os


app = Flask(__name__)

knn_model = joblib.load('knn_model.pkl')
tree_model = joblib.load('decision_tree_model.pkl')
features = joblib.load('features.pkl')
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        logging.debug(f"Received data: {data}")

        model_type = data.get('model', 'tree')
        selected_category = data['features'][0]  # Assuming only one category is selected
        hour = data['hour']
        amount = data['amount']

        # Validate the input
        if not selected_category or hour is None or amount is None:
            raise ValueError("Missing required input fields: 'features', 'hour', or 'amount'")

        # Initialize the feature vector with zeros
        feature_vector = [0] * len(features)

        # Add the 'category_' prefix to the selected category
        if not selected_category.startswith('category_'):
            category_feature = f'category_{selected_category}'
        else:
            category_feature = selected_category

        # Set the selected category to 1
        if category_feature in features:
            feature_vector[features.index(category_feature)] = 1
        else:
            logging.error(f"Feature {category_feature} not found in feature list")
            raise ValueError(f"Invalid category: {selected_category}")

        # Set the hour and amount
        feature_vector[features.index('hour')] = hour
        feature_vector[features.index('amt')] = amount

        # Log the constructed feature vector
        logging.debug(f"Constructed feature vector: {feature_vector}")

        # Make prediction
        if model_type == 'knn':
            prediction = knn_model.predict([feature_vector])
        else:
            prediction = tree_model.predict([feature_vector])

        # Log the prediction
        logging.debug(f"Prediction: {prediction}")

        # Map prediction to label
        prediction_label = "Fraud" if prediction[0] == 1 else "Genuine Transaction"
        if feature_vector[features.index('amt')] > 7699:prediction_label = "Fraud" 
        if feature_vector[features.index('amt')] <= 0:prediction_label = "Please enter a positive value"
        if (feature_vector[features.index('amt')] * 1000) % 1 != 0: prediction_label = "Please enter a valid amount"
        return jsonify({'prediction': prediction_label})

    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return jsonify({'error': 'An error occurred during prediction'}), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/poster')
def poster():
    return render_template('/poster/index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)