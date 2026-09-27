(() => {
  'use strict';
  const esc = value => String(value ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const gallery = [
    ['lena-dialogo','Diálogo com Lena','Diálogos'],['comissao','Comissão diária','Missões'],['barreira','Barreira Temporal','Sistemas'],
    ['offline-ia','Resultado do modo IA offline','Sistemas'],['carregamento','Tela de carregamento','Exploração'],['rift','Rift e chefe Kubaba','Masmorras'],
    ['classe','Tela de classe Assassin','Classes'],['skills','Painel de Skill','Skills'],['cla','Doação ao clã','Clã'],
    ['mapa','Mapa e chefe Karugura','Exploração'],['atributos','Atributos do personagem','Personagem'],['derrota','Tela de derrota','Combate'],['objetivo','Objetivo de masmorra','Tutoriais'],
    ['configuracoes-graficos','Configurações de gráficos','Configurações'],['configuracoes-otimizacao','Configurações de otimização','Configurações']
  ];
  const galleryHost = document.getElementById('gallery');
  galleryHost.innerHTML = gallery.map(([file,title,category]) => `<button class="gallery-item" type="button" data-file="${file}" data-title="${esc(title)}"><img src="images/${file}.webp" alt="${esc(title)}" loading="lazy"><span><small>${esc(category)}</small><strong>${esc(title)}</strong></span></button>`).join('');
  const imageDialog = document.getElementById('image-dialog');
  const feedbackForm = document.getElementById('feedback-form');
  feedbackForm.addEventListener('submit', event => {
    event.preventDefault();
    const type = document.getElementById('feedback-type').value;
    const screen = document.getElementById('feedback-screen').value.trim();
    const message = document.getElementById('feedback-message').value.trim();
    if (!screen || message.length < 10) { feedbackForm.reportValidity(); return; }
    const title = `[${type}] ${screen}`;
    const body = `**Tipo:** ${type}\n**Tela/local:** ${screen}\n\n**Relato e sugestão:**\n${message}\n\n**Captura de tela:** anexe no editor do GitHub antes de publicar.\n\n**Versão do jogo e da tradução:** preencha, se souber.`;
    const url = new URL('https://github.com/jackchakkal/architectlandofexiles_BR/issues/new');
    url.searchParams.set('title', title);
    url.searchParams.set('body', body);
    window.open(url.toString(), '_blank', 'noopener,noreferrer');
  });
  galleryHost.addEventListener('click', event => {
    const button = event.target.closest('[data-file]');
    if (!button) return;
    imageDialog.querySelector('img').src = `images/${button.dataset.file}.webp`;
    imageDialog.querySelector('img').alt = button.dataset.title;
    imageDialog.querySelector('p').textContent = button.dataset.title;
    imageDialog.showModal();
  });
  document.getElementById('close-image').onclick = () => imageDialog.close();
  imageDialog.addEventListener('click', event => { if (event.target === imageDialog) imageDialog.close(); });

  const guides = window.ARCHITECT_GUIDES || [];
  const search = document.getElementById('guide-search');
  const filters = document.getElementById('guide-filters');
  const grid = document.getElementById('guide-grid');
  const more = document.getElementById('guide-more');
  const categories = ['Todos', ...new Set(guides.map(guide => guide.category))];
  let category = 'Todos', count = 12;
  filters.innerHTML = categories.map(value => `<button type="button" class="chip${value === category ? ' active' : ''}" data-category="${esc(value)}">${esc(value)}</button>`).join('');
  function renderGuides() {
    const query = search.value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
    const matches = guides.filter(guide => {
      const text = [guide.title, guide.lead, guide.category, ...guide.steps.map(step => `${step.title} ${step.text}`)].join(' ').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
      return (category === 'Todos' || guide.category === category) && text.includes(query);
    });
    grid.innerHTML = matches.slice(0, count).map(guide => `<button class="guide-card" type="button" data-guide="${esc(guide.id)}"><small>${esc(guide.category)} · ${esc(guide.level)}</small><strong>${esc(guide.title)}</strong><span>${esc(guide.lead)}</span><i>Ler o guia ↗</i></button>`).join('') || '<p>Nenhum guia encontrado. Tente outro termo.</p>';
    more.hidden = matches.length <= count;
  }
  search.oninput = () => { count = 12; renderGuides(); };
  filters.onclick = event => {
    const button = event.target.closest('[data-category]');
    if (!button) return;
    category = button.dataset.category; count = 12;
    filters.querySelectorAll('button').forEach(item => item.classList.toggle('active', item === button));
    renderGuides();
  };
  more.onclick = () => { count += 12; renderGuides(); };
  const guideDialog = document.getElementById('guide-dialog');
  grid.onclick = event => {
    const button = event.target.closest('[data-guide]');
    if (!button) return;
    const guide = guides.find(item => item.id === button.dataset.guide);
    if (!guide) return;
    document.getElementById('guide-detail').innerHTML = `<p class="eyebrow">${esc(guide.category)} · ${esc(guide.level)}</p><h2>${esc(guide.title)}</h2><p class="guide-lead">${esc(guide.lead)}</p>${guide.steps.map((step,index) => `<section><small>PASSO ${String(index + 1).padStart(2,'0')}</small><h3>${esc(step.title)}</h3><p>${esc(step.text)}</p></section>`).join('')}<a href="${esc(guide.source)}" target="_blank" rel="noopener noreferrer">Consultar guia oficial ↗</a>`;
    guideDialog.showModal();
  };
  document.getElementById('close-guide').onclick = () => guideDialog.close();
  guideDialog.addEventListener('click', event => { if (event.target === guideDialog) guideDialog.close(); });
  renderGuides();
})();
