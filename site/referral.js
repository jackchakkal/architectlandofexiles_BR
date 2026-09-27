(() => {
  'use strict';
  document.querySelectorAll('[data-copy-code]').forEach(button => {
    button.addEventListener('click', async () => {
      const code = button.dataset.copyCode;
      const status = button.parentElement.querySelector('.referral-copy-status');
      try {
        if (!navigator.clipboard?.writeText) throw new Error('Clipboard indisponível');
        await navigator.clipboard.writeText(code);
        status.textContent = 'Copiado!';
      } catch {
        status.textContent = `Copie manualmente: ${code}`;
      }
    });
  });
})();
