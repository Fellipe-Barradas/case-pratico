const modal = document.getElementById('emailModal');
const formEmail = document.getElementById('formEmail');

function closeModal() {
    modal.classList.add('hidden');
    clicarEnviarArquivos();
    formEmail.reset();
}

function openModal() {
    modal.classList.remove('hidden');
}

function clicarEnviarArquivos(){
    document.getElementById('fileAttachment').style.display='block';
    document.getElementById('formAttachment').style.display='none';
}

function clicarEnviarTexto(){
    document.getElementById('fileAttachment').style.display='none';
    document.getElementById('formAttachment').style.display='block';
}

formEmail.addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(formEmail);
    console.log('Form Data:', Object.fromEntries(formData.entries()));

    // TODO: Enviar os dados do formulário para o servidor
    closeModal();
    clicarEnviarArquivos();
});