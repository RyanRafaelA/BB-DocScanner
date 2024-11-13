// Seleciona todos os itens do FAQ
const faqItems = document.querySelectorAll('.faq-item');

// Adiciona um evento de clique para cada item do FAQ
faqItems.forEach(item => {
    item.addEventListener('click', () => {
        // Alterna a classe 'active' no item clicado
        item.classList.toggle('active');
        
        // Seleciona a resposta associada
        const answer = item.querySelector('.faq-answer');
        const arrow = item.querySelector('.arrow');

        // Verifica se a resposta está visível e ajusta a exibição
        if (item.classList.contains('active')) {
            answer.style.display = 'block';
            arrow.textContent = '▲'; // Muda a seta para cima
        } else {
            answer.style.display = 'none';
            arrow.textContent = '▼'; // Muda a seta para baixo
        }
    });
});
