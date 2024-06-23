var modelo = null;

//Cargar modelo
(async () => {
    const response = await fetch('decision_tree_model.joblib');
    const modelFile = await response.arrayBuffer();
    const model = await joblib.load(new Uint8Array(modelFile));
    modelo = model; // Asignar el modelo cargado a la variable global
})();

// Funcion donde se realiza la prediccion
function showResult(prediction) {
    var content = document.getElementById("result");
    var image = document.getElementById("imageResult");
    var text = document.getElementById("textResult");

    if (prediction == 0) {
        image.src = "{{ url_for('static', filename='imgs/thumb_down.webp') }}";
        text.textContent = "¡CUIDADO! La oferta de trabajo ingresada es FALSA!";
    } else {
        image.src = "{{ url_for('static', filename='imgs/thumb_up.webp') }}";
        text.textContent = "La oferta de trabajo ingresada es verdadera!";
    }

    content.style.display = "flex";
}

document.addEventListener("DOMContentLoaded", function () {
    var form = document.querySelector("form");
    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Evita que se envíe el formulario de manera convencional

        var formData = new FormData(form);
        fetch('/process-link', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            showResult(data.prediction);
        })
        .catch(error => console.error('Error:', error));
    });
});
