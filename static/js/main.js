document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('cipher-form');
    const buttons = form.querySelectorAll('button[type="submit"]');
    const resultContainer = document.getElementById('result-container');
    const generateSeedBtn = document.getElementById('generate-seed-btn');
    const seedInput = form.elements.seed;

    generateSeedBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/generate-seed');
            const data = await response.json();
            if (data.seed) {
                seedInput.value = data.seed;
            }
        } catch (error) {
            displayError("Failed to generate a new seed. Please try again.");
            console.error('Error generating seed:', error);
        }
    });

    buttons.forEach(button => {
        button.addEventListener('click', async (event) => {
            event.preventDefault();
            resultContainer.innerHTML = ''; // Clear previous results

            const text = form.elements.text.value;
            const seed = seedInput.value;
            const operation = button.value;

            if (!text || !seed) {
                displayError("Lütfen hem metni hem de güvenlik anahtarını girin.");
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
                displayError("Beklenmedik bir hata oluştu. Ayrıntılar için konsola bakın.");
                console.error('Error:', error);
            }
        });
    });

    function displayError(message) {
        resultContainer.innerHTML = `
            <div class="error">
                <p><strong>Hata:</strong> ${message}</p>
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
                // Simple regex to bold the first part of the step
                stepElement.innerHTML = `<p>${step.replace(/^([^:]+:)/, '<strong>$1</strong>')}</p>`;
                stepsContainer.appendChild(stepElement);
                stepElement.scrollIntoView({ behavior: 'smooth', block: 'end' });
            }, delay);
            delay += 300; // Faster step delay
        });

        // Display the final result after all steps
        setTimeout(() => {
            const resultElement = document.createElement('div');
            resultElement.className = 'result';
            resultElement.innerHTML = `
                <h3>Nihai Sonuç:</h3>
                <p>${finalResult}</p>
            `;
            resultContainer.appendChild(resultElement);
            resultElement.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }, delay);
    }
});
