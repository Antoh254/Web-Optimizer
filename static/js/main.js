document.addEventListener('DOMContentLoaded', () => {

    // Tab Switching Logic
    const tabs = document.querySelectorAll('.tab-btn');
    const contents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));

            // Add active class to clicked
            tab.classList.add('active');
            const targetId = tab.getAttribute('data-tab');
            document.getElementById(targetId).classList.add('active');
        });
    });

    // File Input Handling (Generic)
    window.updateCount = function (input, labelId) {
        const label = document.getElementById(labelId);
        const parent = label.parentElement;

        if (input.files.length > 0) {
            const fileCount = input.files.length;
            const text = fileCount === 1 ? '1 File Selected' : `${fileCount} Files Selected`;

            label.innerHTML = `<i style="color: var(--success-color)">✓</i> <b>${text}</b>`;
            parent.classList.add('has-files');
        } else {
            // Reset to default
            const defaultText = labelId === 'imgLabel' ? '📂 Drop images or click to browse' : '📜 Drop CSS/JS or click to browse';
            label.innerHTML = `<i>${labelId === 'imgLabel' ? '🖼️' : '📝'}</i> ${defaultText}`;
            parent.classList.remove('has-files');
        }
    };

    // Quality Slider Logic
    const qualityInput = document.querySelector('input[name="quality"]');
    const qualityValue = document.getElementById('qValue');
    if (qualityInput) {
        qualityInput.addEventListener('input', (e) => {
            qualityValue.innerText = e.target.value;
        });
    }
});
