/* Villa list manager - loads ../data/db.json and renders grid with pagination */
const DB_URL = '../data/db.json';
const PAGE_SIZE_KEY = 'kc_page_size';

const state = { all: [], page: 1, pageSize: parseInt(localStorage.getItem(PAGE_SIZE_KEY)||'24',10) };

async function loadDB(){
  const res = await fetch(DB_URL, { cache:'no-store' });
  if(!res.ok) throw new Error('db.json introuvable');
  const data = await res.json();
  state.all = Array.isArray(data) ? data : (data.villas || []);
  render();
  updateBuildInfo();
}

function updateBuildInfo(){
  const el = document.getElementById('buildInfo');
  if(!el) return;
  const now = new Date();
  el.textContent = `Dernier build: ${now.toLocaleString()} — villas: ${state.all.length}`;
}

function render(){
  const grid = document.getElementById('villaGrid');
  const counter = document.getElementById('counter');
  const start = (state.page-1)*state.pageSize;
  const items = state.all.slice(start, start+state.pageSize);
  counter.textContent = `Affichées ${items.length} / ${state.all.length}`;
  grid.innerHTML = items.map(v=> cardHTML(v)).join('');
  attachImageFallbacks(grid);
  renderPaginator();
}

function cardHTML(v){
  const img = (v.images && v.images[0]) ? v.images[0] : `../images/villas/${v.slug||'villa'}-1.jpg`;
  const alt = v.name ? `Photo de ${v.name}` : 'Photo villa';
  const badge = (v.images && v.images[0]) ? '' : '<span class="badge">Photo à venir</span>';
  return `<article class="card">
    <img src="${img}" alt="${alt}" onerror="this.onerror=null;this.src='../images/placeholder_villa.webp'">
    <div class="body">
      <h4>${v.name||'Villa'}</h4>
      <div>${v.location||''} ${badge}</div>
      <div style="margin:6px 0"><strong>${formatPrice(v.pricePerNight)}</strong> / nuit</div>
      <div style="opacity:.9">${(v.bedrooms||'?')} ch • ${(v.bathrooms||'?')} sdb • ${(v.surface||'?')} m²</div>
    </div>
  </article>`;
}

function formatPrice(x){
  const n = Number(x||0); return isFinite(n) ? new Intl.NumberFormat('fr-FR',{style:'currency',currency:'EUR'}).format(n) : '—';
}

function renderPaginator(){
  const pages = Math.max(1, Math.ceil(state.all.length / state.pageSize));
  const c = document.getElementById('paginator');
  const btn = (p,txt)=>`<button ${p===state.page?'disabled':''} data-p="${p}">${txt}</button>`;
  c.innerHTML = `${btn(1,'⏮')} ${btn(Math.max(1,state.page-1),'◀')} <span style="padding:6px 10px">Page ${state.page}/${pages}</span> ${btn(Math.min(pages,state.page+1),'▶')} ${btn(pages,'⏭')}`;
  c.querySelectorAll('button[data-p]').forEach(b=> b.addEventListener('click',()=>{ state.page=parseInt(b.dataset.p,10); render(); }));
}

// Page size selector
(function(){
  const sel = document.getElementById('pageSize');
  if(!sel) return;
  // set from storage
  Array.from(sel.options).forEach(o=>{ if(parseInt(o.value||o.text,10)===state.pageSize) o.selected=true; });
  sel.addEventListener('change', ()=>{ state.pageSize=parseInt(sel.value,10); localStorage.setItem(PAGE_SIZE_KEY,String(state.pageSize)); state.page=1; render(); });
})();

// Init
loadDB().catch(()=>{
  const grid = document.getElementById('villaGrid');
  if(grid){ grid.innerHTML = '<p>Impossible de charger les données (db.json)</p>'; }
});