document.getElementById('uploadForm').addEventListener('submit', async(e) =>{
    e.preventDefault();

    const formData = new FormData();
    const file = document.getElementById('file');
    const message = document.getElementById('message');

    formData.append('file', file.files[0]);
    formData.append('message', message.value);

    try{
        const response = await fetch('http://127.0.0.1:5000/scan', {
            method: 'POST',
            body: formData
        });
        
        if(!response.ok) {
            throw new Error('Erro no processamento do arquivo.')
        }

        const result = await response.json();

        window.location.href = `result.html?data=${encodeURIComponent(JSON.stringify(result))}`;
    } catch(error) {
        alert('erro: ' + error.message)
    }
});