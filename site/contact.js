(() => {
  'use strict';
  const form = document.getElementById('private-form');
  const status = document.getElementById('contact-status');
  const button = form.querySelector('button[type="submit"]');
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    button.disabled = true;
    status.className = 'form-status';
    status.textContent = 'Enviando sua mensagem…';
    try {
      const response = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      });
      if (!response.ok) throw new Error('Falha no envio');
      form.reset();
      status.className = 'form-status success';
      status.textContent = 'Mensagem enviada. Obrigado pelo contato! / Message sent. Thank you!';
    } catch {
      status.className = 'form-status error';
      status.textContent = 'Não foi possível enviar agora. Tente novamente mais tarde. / Could not send right now. Please try again later.';
    } finally {
      button.disabled = false;
    }
  });
})();
