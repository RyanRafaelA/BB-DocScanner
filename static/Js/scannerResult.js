const urlParam = new URLSearchParams(window.location.search);
const data = urlParam.get('data');

if(data){
    const result = JSON.parse(decodeURIComponent(data));

    const resultContainer = document.querySelector('.info-documento');
    resultContainer.innerHTML = `<p>${result.result}</p>`;
} else {
    alert('Nenhum dado recebido!');
}