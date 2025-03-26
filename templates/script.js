document.getElementById('predict-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const selectedOptions = document.getElementById('features').selectedOptions;
    const features = Array.from(selectedOptions).map(option => option.value);
    const amount = parseFloat(document.getElementById('amount').value);
    const model = document.getElementById('model').value;
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ features: features, amount: amount, model: model })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = 'Prediction: ' + data.prediction;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});