(function(){
  if(typeof window==='undefined') return;
  const PREFIX='kc:';
  const WHITELIST={
    'kc:consent': 365*24*60*60*1000,
    'kc:ui:lang': 365*24*60*60*1000,
    'kc:ui:theme': 365*24*60*60*1000,
    'kc:cache:': 24*60*60*1000 // prefix
  };
  function ttlFor(key){
    if(key.startsWith('kc:cache:')) return WHITELIST['kc:cache:'];
    return WHITELIST[key] || 0;
  }
  function allowed(key){
    return key==='kc:consent' || key==='kc:ui:lang' || key==='kc:ui:theme' || key.startsWith('kc:cache:');
  }
  function banner(msg){
    const b=document.querySelector('.api-banner')||(function(){const d=document.createElement('div');d.className='api-banner';d.style.cssText='position:fixed;bottom:10px;left:10px;background:rgba(0,0,0,.7);color:#fff;padding:6px 10px;border-radius:8px;font-size:12px;z-index:9999';document.body.appendChild(d);return d;})();
    b.textContent=msg;
  }
  const kcStorage={
    set(key, value){
      try{
        if(!allowed(key)) { console.warn('[kcStorage] blocked write for', key); return false; }
        const ttl=ttlFor(key);
        const payload={v:value, createdAt: Date.now(), ttl};
        localStorage.setItem(key, JSON.stringify(payload));
        return true;
      }catch(e){ console.warn('[kcStorage] set error', e); return false; }
    },
    get(key){
      try{
        const raw=localStorage.getItem(key);
        if(!raw) return null;
        const obj=JSON.parse(raw);
        if(obj && obj.ttl){
          const age=Date.now() - (obj.createdAt||0);
          if(age>obj.ttl){ localStorage.removeItem(key); return null; }
        }
        return obj ? obj.v : null;
      }catch(e){ return null; }
    },
    remove(key){ try{ localStorage.removeItem(key); }catch(_){}}
  };
  window.kcStorage=kcStorage;

  // Runtime purge via query
  const qs=window.location.search.substring(1).split('&').reduce((a,p)=>{const [k,v]=p.split('='); if(k) a[decodeURIComponent(k)]=decodeURIComponent(v||''); return a;},{});
  if(qs.purge_storage==='1'){
    try{
      Object.keys(localStorage).forEach(k=>{ if(k.startsWith(PREFIX)) localStorage.removeItem(k); });
      banner('Stockage local purgé');
    }catch(_){}
  }
})();
