// Funções para manipular modal
function openModal() {
    document.getElementById('emailModal').classList.remove('hidden');
}
function closeModal() {
    document.getElementById('emailModal').classList.add('hidden');
    clicarEnviarArquivos();
    document.getElementById('formEmail').reset();
}

function clicarEnviarArquivos() {
    document.getElementById('fileAttachment').classList.remove('hidden');
    document.getElementById('formAttachment').classList.add('hidden');
}
function clicarEnviarTexto() {
    document.getElementById('fileAttachment').classList.add('hidden');
    document.getElementById('formAttachment').classList.remove('hidden');
}


let currentPage = 1;
let pageSize = 10;
let totalEmails = 0;
let totalPages = 1;
let currentTipoEmailId = '';
let tiposEmail = [];

async function fetchEmails() {
    let url = `http://localhost:8000/obter-emails?size=${pageSize}&step=${currentPage}`;
    if (currentTipoEmailId) {
        url += `&tipo_email_id=${currentTipoEmailId}`;
    }
  
    try {
        const res = await fetch(url);
        const data = await res.json();
        renderEmails(data.data);
        // Tenta obter o total de emails do backend, se disponível
        if (data.total !== undefined) {
            totalEmails = data.total;
        } else {
            // fallback: se backend não retorna total, estima pelo tamanho da página
            totalEmails = (data.data.length < pageSize && currentPage > 1) ? ((currentPage - 1) * pageSize + data.data.length) : (currentPage * pageSize);
        }
        totalPages = Math.max(1, Math.ceil(totalEmails / pageSize));
        updatePaginationInfo(data.data.length);
    } catch (err) {
        console.error('Erro ao buscar emails:', err);
    }
}

function updatePaginationInfo(count) {
    const info = document.getElementById('paginationInfo');
    info.textContent = `Página ${currentPage}`;
    const totalInfo = document.getElementById('totalPagesInfo');
    totalInfo.textContent = `/ ${totalPages} páginas`;
    document.getElementById('prevPage').disabled = currentPage === 1;
    document.getElementById('nextPage').disabled = count < pageSize;
}

async function fetchTiposEmail() {
    try {
        const res = await fetch('http://localhost:8000/tipos-email');
        const data = await res.json();
        tiposEmail = data.data;
        renderTiposEmailFilter();
    } catch (err) {
        console.error('Erro ao buscar tipos de email:', err);
    }
}

function renderTiposEmailFilter() {
    const select = document.getElementById('tipoEmailFilter');
    select.innerHTML = '<option value="">Todos</option>';
    tiposEmail.forEach(tipo => {
        select.innerHTML += `<option value="${tipo.id}">${tipo.nome}</option>`;
    });
    select.value = currentTipoEmailId;
}

function deletarEmail(id){
    fetch(`http://localhost:8000/delete-email?id=${id}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (!response.ok) throw new Error('Erro ao deletar email');
        fetchEmails();
    })
    .catch(err => {
        console.error(err);
    });
}

// Renderiza emails na tabela
function renderEmails(emails) {
    const tbody = document.querySelector('table tbody');
    tbody.innerHTML = '';
    if (!emails || emails.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" class="py-2 px-4 text-center">Nenhum email encontrado.</td></tr>';
        return;
    }
    emails.forEach(email => {
        const tr = document.createElement('tr');
        tr.className = 'border-t';
        tr.innerHTML = `
            <td class="py-2 px-4">${email.assunto || ''}</td>
            <td class="py-2 px-4">${email.criado_em ? new Date(email.criado_em).toLocaleDateString() : ''}</td>
            <td class="py-2 px-4" style="color: ${email.tipo_email === 'produtivo' ? 'green' : email.tipo_email === 'improdutivo' ? 'red' : 'inherit'};">${email.tipo_email || ''}</td>
            <td class="py-2 px-4">
            ${email.resposta || ''}
            </td>
            <td class="py-2 px-4">
            <button class="text-red-600 hover:text-red-800" onclick="deletarEmail(${email.id})" title="Deletar" style="cursor:pointer;">
            Deletar
            </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Submete o formulário de envio de email
async function enviarEmail(event) {
    event.preventDefault();
    const tipo = document.querySelector('input[name="attachmentType"]:checked').value;
    const formData = new FormData();
    if (tipo === 'file') {
        const fileInput = document.getElementById('attachment');
        if (fileInput.files.length === 0) {
            alert('Selecione um arquivo!');
            return;
        }
        formData.append('file', fileInput.files[0]);
    } else {
        const emailText = document.getElementById('attachmentText').value;
        if (!emailText.trim()) {
            alert('Digite o conteúdo do email!');
            return;
        }
        formData.append('email', emailText);
    }
    try {
        const res = await fetch(`http://localhost:8000/analisar-email`, {
            method: 'POST',
            body: formData
        });
        if (!res.ok) throw new Error('Erro ao enviar email');
        closeModal();
        fetchEmails();
    } catch (err) {
        alert('Erro ao enviar email!');
        console.error(err);
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    await fetchEmails();
    await fetchTiposEmail();
    document.getElementById('formEmail').addEventListener('submit', enviarEmail);
    document.getElementById('prevPage').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            fetchEmails();
        }
    });
    document.getElementById('nextPage').addEventListener('click', () => {
        currentPage++;
        fetchEmails();
    });
    document.getElementById('tipoEmailFilter').addEventListener('change', (e) => {
        currentTipoEmailId = e.target.value;
        currentPage = 1;
        fetchEmails();
    });
    document.getElementById('pageSizeSelect').addEventListener('change', (e) => {
        pageSize = parseInt(e.target.value);
        currentPage = 1;
        fetchEmails();
    });

    // Carrossel tutorial
    let carouselIndex = 0;
    const slides = document.querySelectorAll('#carouselSlides .carousel-slide');
    const nextBtn = document.getElementById('carouselNext');
    const prevBtn = document.getElementById('carouselPrev');
    const closeBtn = document.getElementById('closeCarousel');
    const carousel = document.getElementById('tutorialCarousel');

    function showSlide(idx) {
        slides.forEach((slide, i) => {
            slide.classList.toggle('hidden', i !== idx);
        });
        if (idx === 0) {
            prevBtn.disabled = true;
            prevBtn.style.display = 'none';
        } else {
            prevBtn.disabled = false;
            prevBtn.style.display = 'block';
        }
        if (idx === slides.length - 1){
             nextBtn.disabled = true;
             nextBtn.style.display = 'none';
        } else {
            nextBtn.disabled = false;
            nextBtn.style.display = 'block';
        }
       
    }
    if (carousel) {
        showSlide(carouselIndex);
        nextBtn.addEventListener('click', () => {
            if (carouselIndex < slides.length - 1) {
                carouselIndex++;
                showSlide(carouselIndex);
            }
        });
        prevBtn.addEventListener('click', () => {
            if (carouselIndex > 0) {
                carouselIndex--;
                showSlide(carouselIndex);
            }
        });
        closeBtn.addEventListener('click', () => {
            carousel.classList.add('hidden');
        });
    }
});