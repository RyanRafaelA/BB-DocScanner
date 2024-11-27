document.getElementById('uploadForm').addEventListener('submit', async(e) =>{
    e.preventDefault();

    const formData = new FormData();
    const file = document.getElementById('file');
    const message = document.getElementById('message');

    formData.append('file', file.files[0]);
    formData.append('message', message.value);

    try{
        const response = await fetch('https://techdoc.onrender.com/scan', { 
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
