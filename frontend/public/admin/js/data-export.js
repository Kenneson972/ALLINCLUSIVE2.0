/* Import/Export JSON + Export CSV */
const exportJSONBtn = document.getElementById('exportJson');
const exportCSVBtn = document.getElementById('exportCsv');
const importInput = document.getElementById('importJson');
const importReport = document.getElementById('importReport');

exportJSONBtn?.addEventListener('click', ()=>{
  const blob = new Blob([JSON.stringify(state.all,null,2)], { type:'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  const d = new Date();
  a.download = `khanel_villas_export_${d.getFullYear()}${String(d.getMonth()+1).padStart(2,'0')}${String(d.getDate()).padStart(2,'0')}.json`;
  a.click();
});

exportCSVBtn?.addEventListener('click', ()=>{
  const cols = ['id','name','status','pricePerNight','city','bedrooms','bathrooms','surface','imageCount'];
  const lines = [cols.join(',')];
  state.all.forEach(v=>{
    const row = [v.id,v.name,v.status,v.pricePerNight,v.city||'',v.bedrooms||'',v.bathrooms||'',v.surface||'',(v.images||[]).length];
    lines.push(row.map(x=>`"${String(x??'').replace(/"/g,'""')}"`).join(','));
  });
  const blob = new Blob([lines.join('\n')], { type:'text/csv' });
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'khanel_villas_export.csv'; a.click();
});

importInput?.addEventListener('change', async (e)=>{
  const file = e.target.files?.[0]; if(!file) return;
  try{
    const text = await file.text();
    const arr = JSON.parse(text);
    if(!Array.isArray(arr)) throw new Error('JSON attendu: tableau de villas');
    const byKey = new Map(state.all.map(v=>[(v.id||v.slug), v]));
    let added=0, updated=0;
    arr.forEach(v=>{
      const key = (v.id||v.slug);
      if(!key){ return; }
      if(byKey.has(key)){
        Object.assign(byKey.get(key), v); updated++;
      } else {
        state.all.push(v); byKey.set(key,v); added++;
      }
    });
    importReport.textContent = `Import terminé — Ajoutés: ${added}, Mis à jour: ${updated}`;
    state.page=1; render(); updateBuildInfo();
  }catch(err){ importReport.textContent = 'Erreur import: '+err.message; }
});