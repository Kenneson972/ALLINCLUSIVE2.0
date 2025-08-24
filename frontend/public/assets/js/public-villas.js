/* Public villas renderer - reads ./data/db.json with cache-busting, renders grid with filters + pagination */
(function(){
  const S = sel => document.querySelector(sel);
  const grid = S('#villas-grid'), counter = S('#counter'), pinfo = S('#pinfo');
  const q = S('#q'), citySel = S('#city'), pageSizeSel = S('#pageSize');
  const prevBtn = S('#prev'), nextBtn = S('#next');
  const PAGE_SIZE_KEY = 'villas_pageSize';
  let data=[], view=[], page=1, pageSize= +localStorage.getItem(PAGE_SIZE_KEY) || 12;

  function formatPrice(n){
    n = Number(n||0); return isFinite(n) ? new Intl.NumberFormat('fr-FR',{style:'currency',currency:'EUR'}).format(n) : '—';
  }
  function hydrateCities(list){
    const values = [...new Set(list.map(v => (v.location?.city||v.location||'').split(',')[0].trim()).filter(Boolean))].sort();
    values.forEach(c=>{ const o=document.createElement('option'); o.value=o.textContent=c; citySel.appendChild(o); });
  }
  function applyFilters(){
    const term=(q?.value||'').toLowerCase();
    const city=citySel?.value||'';
    view = data.filter(v=>{
      const hit = (v.name||'').toLowerCase().includes(term) || (v.location||'').toLowerCase().includes(term);
      const okCity = !city || (v.location||'').toLowerCase().includes(city.toLowerCase());
      return hit && okCity;
    });
  }
  function render(){
    const start=(page-1)*pageSize, end=start+pageSize;
    const pageItems = view.slice(start, end);
    const total=view.length; const shown=pageItems.length;
    if(counter) counter.textContent = `Affichées ${shown} / ${total}`;
    if(grid) grid.innerHTML = pageItems.map(cardHTML).join('');
    attachImageFallbacks(grid);
    const pages = Math.max(1, Math.ceil(total/pageSize));
    if(pinfo) pinfo.textContent = `Page ${page} / ${pages}`;
    prevBtn.disabled = page<=1; nextBtn.disabled = page>=pages;
  }
  function cardHTML(v){
    const img = (v.images && v.images[0]) ? v.images[0] : './assets/images/placeholders/villa-placeholder.jpg';
    const alt = v.name ? `Photo de ${v.name}` : 'Villa';
    return `<article class="villa-card">
      <img class="villa-image" src="${img}" alt="${alt}" loading="lazy" onerror="this.src='./assets/images/placeholders/villa-placeholder.jpg'">
      <div class="villa-info">
        <div class="villa-name">${v.name||'Villa'}</div>
        <div class="villa-location"><i class="fas fa-map-marker-alt"></i> ${v.location||''}</div>
        <div class="villa-features"><span><i class="fas fa-users"></i> ${v.bedrooms||'?'} pers</span> <span><i class="fas fa-bed"></i> ${v.bedrooms||'?'} ch</span> <span><i class="fas fa-swimming-pool"></i> Piscine</span></div>
        <div class="villa-price">${formatPrice(v.pricePerNight)} / nuit</div>
        <div><span class="btn btn-outline-gold">Voir la villa</span></div>
      </div>
    </article>`;
  }

  function attach(){
    pageSizeSel.value = pageSize;
    q?.addEventListener('input', ()=>{ page=1; applyFilters(); render(); });
    citySel?.addEventListener('change', ()=>{ page=1; applyFilters(); render(); });
    pageSizeSel?.addEventListener('change', e=>{ pageSize=+e.target.value; localStorage.setItem(PAGE_SIZE_KEY, pageSize); page=1; render(); });
    prevBtn?.addEventListener('click', ()=>{ if(page>1){ page--; render(); } });
    nextBtn?.addEventListener('click', ()=>{ page++; render(); });
  }

  fetch('./data/db.json?v=' + Date.now())
    .then(r=>r.json())
    .then(db=>{ data = Array.isArray(db)?db:(db.villas||[]); hydrateCities(data); attach(); applyFilters(); render(); })
    .catch(()=>{ if(grid) grid.innerHTML = '<p>Impossible de charger les villas.</p>'; });
})();