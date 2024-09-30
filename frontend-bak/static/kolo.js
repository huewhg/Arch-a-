const wheel = document.getElementById('wheel');
const spinButton = document.getElementById('spinButton');
const resultDiv = document.getElementById('result');
const resultTitle = resultDiv.querySelector('h2');
const resultTask = resultDiv.querySelector('p');

const categories = ['Art', 'Music', 'Theater', 'Dance'];
const tasks = {
    'Art': 'Draw a self-portrait using only primary colors',
    'Music': 'Compose a short melody inspired by your favorite season',
    'Theater': 'Write and perform a one-minute monologue about your hero',
    'Dance': 'Create a 30-second dance routine to your favorite song'
};

let rotation = 0;
let spinning = false;

spinButton.addEventListener('click', () => {
    if (spinning) return;
    spinning = true;
    resultDiv.classList.add('hidden');
    spinButton.textContent = 'Spinning...';
    spinButton.disabled = true;

    const newRotation = rotation + 360 * 5 + Math.random() * 360;
    wheel.style.transform = `rotate(${newRotation}deg)`;

    setTimeout(() => {
        spinning = false;
        spinButton.textContent = 'Spin the Wheel';
        spinButton.disabled = false;

        const index = Math.floor(((newRotation % 360) / 360) * categories.length);
        const result = categories[index];

        resultTitle.textContent = `Kaydem 3's Task: ${result}`;
        resultTask.textContent = tasks[result];
        resultDiv.classList.remove('hidden');

        rotation = newRotation;
    }, 5000);
});