document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('cipher-form');
    const buttons = form.querySelectorAll('button');
    const resultContainer = document.getElementById('result-container');

    buttons.forEach(button => {
        button.addEventListener('click', async (event) => {
            event.preventDefault();
            resultContainer.innerHTML = ''; // Clear previous results

            const text = form.elements.text.value;
            const seed = form.elements.seed.value;
            const operation = button.value;

            if (!text || !seed) {
                displayError("Please provide both text and a seed.");
                return;
            }

            // Show loading spinner
            const spinner = document.createElement('div');
            spinner.className = 'spinner';
            resultContainer.appendChild(spinner);

            try {
                const response = await fetch('/process', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text, seed, operation }),
                });

                const data = await response.json();
                resultContainer.innerHTML = ''; // Clear spinner

                if (data.error) {
                    displayError(data.error);
                } else {
                    displaySteps(data.steps, data.result);
                }

            } catch (error) {
                resultContainer.innerHTML = ''; // Clear spinner
                displayError("An unexpected error occurred. See console for details.");
                console.error('Error:', error);
            }
        });
    });

    function displayError(message) {
        resultContainer.innerHTML = `
            <div class="error">
                <p><strong>Error:</strong> ${message}</p>
            </div>
        `;
    }

    function displaySteps(steps, finalResult) {
        const stepsContainer = document.createElement('div');
        stepsContainer.className = 'steps-container';
        resultContainer.appendChild(stepsContainer);

        let delay = 0;
        steps.forEach((step, index) => {
            setTimeout(() => {
                const stepElement = document.createElement('div');
                stepElement.className = 'step';
                stepElement.innerHTML = `<p>${step}</p>`;
                stepsContainer.appendChild(stepElement);
                stepElement.scrollIntoView({ behavior: 'smooth', block: 'end' });
            }, delay);
            delay += 500; // 0.5 second delay between steps
        });

        // Display the final result after all steps
        setTimeout(() => {
            const resultElement = document.createElement('div');
            resultElement.className = 'result';
            resultElement.innerHTML = `
                <h2>Final Result:</h2>
                <p>${finalResult}</p>
            `;
            resultContainer.appendChild(resultElement);
            resultElement.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }, delay);
    }
});
