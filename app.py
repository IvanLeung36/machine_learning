from flask import Flask, request, jsonify, render_template
import joblib
import logging

app = Flask(__name__)

knn_model = joblib.load('knn_model.pkl')
tree_model = joblib.load('decision_tree_model.pkl')

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    logging.debug(f"Received data: {data}")
    model_type = data.get('model', 'tree')
    features = data['features']
    amount = data['amount']
    feature_vector = [0] * 13
    for feature in features:
        try:
            index = features.index(feature)
            feature_vector[index] = 1
        except ValueError:
            logging.error(f"Feature {feature} not found in feature list")
    feature_vector.append(amount)
    logging.debug(f"Feature vector: {feature_vector}")

    if model_type == 'knn':
        prediction = knn_model.predict([feature_vector])
    else:
        prediction = tree_model.predict([feature_vector])

    logging.debug(f"Prediction: {prediction}")

    prediction_label = "Fraud" if prediction[0] == 1 else "Genuine Transaction"

    return jsonify({'prediction': prediction_label})

if __name__ == '__main__':
    app.run(debug=True)