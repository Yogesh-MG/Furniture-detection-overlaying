document.addEventListener('DOMContentLoaded', () => {
    const originalImage = document.getElementById('original-image');
    const predictedImage = document.getElementById('predicted-image');
    const loadingOriginal = document.getElementById('loading-original');
    const loadingPredicted = document.getElementById('loading-predicted');

    if (originalImage) {
        loadingOriginal.style.display = 'none';
    } else {
        loadingOriginal.style.display = 'block';
    }

    if (predictedImage) {
        loadingPredicted.style.display = 'none';
    } else {
        loadingPredicted.style.display = 'block';
    }
});
    
