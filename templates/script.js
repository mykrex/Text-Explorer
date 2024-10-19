const fileInput = document.getElementById('fileInput');
const loadButton = document.getElementById('loadButton');
const fileStatus = document.getElementById('fileStatus');
const fileContentsContainer = document.getElementById('fileContentsContainer');
const fileContent1 = document.getElementById('fileContent1');
const fileContent2 = document.getElementById('fileContent2');
const similarityButton = document.getElementById('similarityButton');
const kmpButton = document.getElementById('kmpButton');
const manacherButton = document.getElementById('manacherButton');
const autocompletarInput = document.getElementById('autocompletar_input');
const suggestionsList = document.getElementById('suggestions');

let selectedFiles = [];

fileInput.addEventListener('change', (e) => {
    selectedFiles = Array.from(e.target.files);
    loadButton.disabled = selectedFiles.length === 0;
    fileStatus.textContent = selectedFiles.length > 0 ? `${selectedFiles.length} archivo(s) seleccionado(s)` : 'No se ha cargado un archivo';
});

loadButton.addEventListener('click', () => {
    if (selectedFiles.length > 0) {
        const reader1 = new FileReader();
        reader1.onload = (e) => {
            fileContent1.textContent = e.target.result;
            fileContentsContainer.style.display = 'flex';
            kmpButton.disabled = false;
            manacherButton.disabled = false;
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
            fileContent2.style.display = 'none';
            similarityButton.disabled = true;
        }

        // Cargar el archivo para auto-completar
        const formData = new FormData();
        formData.append('archivo', selectedFiles[0]);
        fetch('/cargar', {
            method: 'POST',
            body: formData
        })
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
    fetch('/similitud', {
        method: 'POST',
        body: formData
    })
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

let currentSelection = -1;

autocompletarInput.addEventListener('input', function() {
    const query = this.value;
    const lastWord = query.split(/\s+/).pop();
    
    if (lastWord) {
        fetch(`/autocompletar?prefix=${lastWord}`)
            .then(response => response.json())
            .then(data => {
                suggestionsList.innerHTML = '';
                data.forEach((item, index) => {
                    const li = document.createElement('li');
                    li.textContent = `${item.word} (${item.frequency})`;
                    li.addEventListener('click', function() {
                        const words = autocompletarInput.value.split(/\s+/);
                        words[words.length - 1] = item.word;
                        autocompletarInput.value = words.join(' ') + ' ';
                        suggestionsList.innerHTML = '';
                        autocompletarInput.focus();
                    });
                    suggestionsList.appendChild(li);
                });
                currentSelection = -1;
            });
    } else {
        suggestionsList.innerHTML = '';
    }
});

autocompletarInput.addEventListener('keydown', function(e) {
    const suggestions = suggestionsList.querySelectorAll('li');
    
    if (e.key === 'ArrowDown') {
        currentSelection = (currentSelection + 1) % suggestions.length;
        updateSelection();
        e.preventDefault();
    } else if (e.key === 'ArrowUp') {
        currentSelection = (currentSelection - 1 + suggestions.length) % suggestions.length;
        updateSelection();
        e.preventDefault();
    } else if (e.key === 'Enter' && currentSelection !== -1) {
        const selectedWord = suggestions[currentSelection].textContent.split(' ')[0];
        const words = autocompletarInput.value.split(/\s+/);
        words[words.length - 1] = selectedWord;
        autocompletarInput.value = words.join(' ') + ' ';
        suggestionsList.innerHTML = '';
        e.preventDefault();
    }
});

function updateSelection() {
    const suggestions = suggestionsList.querySelectorAll('li');
    suggestions.forEach((suggestion, index) => {
        if (index === currentSelection) {
            suggestion.classList.add('selected');
            suggestion.scrollIntoView({ block: 'nearest' });
        } else {
            suggestion.classList.remove('selected');
        }
    });
}