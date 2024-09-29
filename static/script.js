// Previsualización de las imágenes seleccionadas
function previewImages() {
    const previewContainer = document.getElementById('preview-container');
    previewContainer.innerHTML = '';
    const files = document.getElementById('image').files;

    Array.from(files).forEach(file => {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            previewContainer.appendChild(img);
        };
        reader.readAsDataURL(file);
    });
}

// Actualiza el valor de la calidad en el slider
document.getElementById('quality').addEventListener('input', function() {
    document.getElementById('qualityValue').textContent = this.value;
});
