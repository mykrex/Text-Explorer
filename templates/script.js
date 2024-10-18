const fileInput = document.getElementById('fileInput');
const loadButton = document.getElementById('loadButton');
const fileContent1 = document.getElementById('fileContent1');
const fileContent2 = document.getElementById('fileContent2');
const similarityButton = document.getElementById('similarityButton');

let selectedFiles = [];

fileInput.addEventListener('change', (e) => {
    selectedFiles = Array.from(e.target.files);
    loadButton.disabled = selectedFiles.length === 0;
});

loadButton.addEventListener('click', () => {
    if (selectedFiles.length > 0) {
        const reader1 = new FileReader();
        reader1.onload = (e) => {
            fileContent1.textContent = e.target.result;
            fileContent1.style.display = 'block';
        };
        reader1.readAsText(selectedFiles[0]);

        if (selectedFiles.length > 1) {
            const reader2 = new FileReader();
            reader2.onload = (e) => {
                fileContent2.textContent = e.target.result;
                fileContent2.style.display = 'block';
                similarityButton.disabled = false;
            };
            reader2.readAsText(selectedFiles[1]);
        } else {
            fileContent2.textContent = '';
            similarityButton.disabled = true;
        }

        // Cargar el archivo para auto-completar
        const formData = new FormData();
        formData.append('archivo', selectedFiles[0]);
        fetch('/cargar', { method: 'POST', body: formData })
            .then(response => response.json())
            .then(data => {
                console.log(data.message + ' ' + data.palabras_cargadas + ' palabras cargadas.');
            });
    }
});

similarityButton.addEventListener('click', () => {
    const formData = new FormData();
    formData.append('archivo1', selectedFiles[0]);
    formData.append('archivo2', selectedFiles[1]);
    fetch('/similitud', { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => {
            highlightLCS(data.subcadena_comun);
        });
});

function highlightLCS(lcs) {
    const content1 = fileContent1.textContent;
    const content2 = fileContent2.textContent;

    const regex = new RegExp(lcs, 'g');
    fileContent1.innerHTML = content1.replace(regex, `<span class="highlight">${lcs}</span>`);
    fileContent2.innerHTML = content2.replace(regex, `<span class="highlight">${lcs}</span>`);
}

document.getElementById('autocompletar_input').addEventListener('input', function() {
    const query = this.value;
    fetch(`/autocompletar?prefix=${query}`)
        .then(response => response.json())
        .then(data => {
            const suggestionsList = document.getElementById('suggestions');
            suggestionsList.innerHTML = '';
            data.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `${item.word} (${item.frequency})`;
                li.addEventListener('click', function() {
                    document.getElementById('autocompletar_input').value = item.word;
                    suggestionsList.innerHTML = '';
                });
                suggestionsList.appendChild(li);
            });
        });
});