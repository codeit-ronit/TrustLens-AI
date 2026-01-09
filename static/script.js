/**
 * Function to analyze reviews from a given product URL.
 * It sends the URL to the backend for review scraping and classification,
 * then displays the results on the webpage.
 */
function analyzeReviews() {
    const url = document.getElementById("url").value; // Get the entered product URL
    const resultDiv = document.getElementById("result"); // Result display area
    const loadingDiv = document.getElementById("loading"); // Loading indicator

    // Validate if the user entered a URL
    if (!url) {
        resultDiv.innerHTML = "<p style='color: red;'>⚠ Please enter a valid product URL.</p>";
        return;
    }

    resultDiv.innerHTML = ""; // Clear previous results
    loadingDiv.style.display = "block"; // Show loading animation

    // Send the request to the backend API for review analysis
    // fetch("/analyze", {
    //     method: "POST",
    //     headers: { "Content-Type": "application/json" },
    //     body: JSON.stringify({ url: url })
    // })
    fetch("/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json()) // Convert the response to JSON
    .then(data => {
        loadingDiv.style.display = "none"; // Hide loading animation
        
        // Handle errors from the backend
        if (data.error) {
            resultDiv.innerHTML = `<p style='color: red;'>⚠ ${data.error}</p>`;
        } else {
            let html = "<h2>Results</h2><div class='review-container'>";
            
            // Loop through the received reviews and generate HTML content
            data.forEach(review => {
                const predictionClass = review.Prediction === "Real (Original)" ? "real" : "fake";
                html += `
                    <div class="review-card">
                        <p class="review-text"><strong>Review:</strong> ${review.Review}</p>
                        <p class="review-rating"><strong>Rating:</strong> ⭐ ${review.Rating}</p>
                        <p class="review-prediction ${predictionClass}">
                            <strong>Prediction:</strong> ${review.Prediction}
                        </p>
                    </div>
                `;
            });
            
            html += "</div>";
            resultDiv.innerHTML = html; // Display the reviews and predictions
        }
    })
    .catch(error => {
        loadingDiv.style.display = "none"; // Hide loading animation on error
        resultDiv.innerHTML = "<p style='color: red;'>⚠ Error processing request.</p>";
    });
}
