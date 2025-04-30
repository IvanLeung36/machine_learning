document.addEventListener("DOMContentLoaded", function () {
    const predictionForm = document.getElementById("predictionForm");
    const resultCard = document.getElementById("resultCard");
    const resultContent = document.getElementById("resultContent");
    const amountInput = document.getElementById("amount");
    const amountWarning = document.getElementById("amount-warning");

    function checkAmount() {
        const amount = parseFloat(amountInput.value);
        if (!isNaN(amount) && amount > AMOUNT_THRESHOLD) {
            amountWarning.classList.remove("d-none");
        } else {
            amountWarning.classList.add("d-none");
        }
    }

    amountInput.addEventListener("input", checkAmount);

    predictionForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(predictionForm);

        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            resultCard.classList.remove("d-none");

            if (data.error) {
                resultContent.innerHTML = `
                <div class="alert alert-danger">
                    <strong>Error:</strong> ${data.error}
                </div>`;
            } else {
                const isFraud = data.prediction;
                const probability = (data.probability * 100).toFixed(2);
                const modelUsed = data.model_used === 'knn' ? 'K-Nearest Neighbors' : 'Decision Tree';

                let alertClass = isFraud ? "alert-danger" : "alert-success";
                let predictionText = isFraud ? "Potentially Fraudulent" : "Likely Legitimate";

                resultContent.innerHTML = `
                <div class="alert ${alertClass}">
                    <h4 class="alert-heading">Prediction: ${predictionText}</h4>
                    <p>Fraud probability: ${probability}%</p>
                    <hr>
                    <p class="mb-0">Model used: ${modelUsed}</p>
                </div>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultCard.classList.remove("d-none");
            resultContent.innerHTML = `
            <div class="alert alert-danger">
                <strong>Error:</strong> An unexpected error occurred. Please try again.
            </div>`;
        });
    });
});
