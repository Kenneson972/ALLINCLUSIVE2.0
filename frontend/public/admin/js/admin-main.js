/* Auth + Config loader (static, GitHub Pages friendly) */
const KC_CFG_URL = './config.json';
const KC_TOKEN_KEY = 'kc_admin_token';
const KC_FAIL_KEY = 'kc_login_fails';
const KC_BLOCK_KEY = 'kc_login_block_until';

async function sha256Hex(text){
  const enc = new TextEncoder();
  const data = enc.encode(text);
  const hash = await crypto.subtle.digest('SHA-256', data);
  const bytes = Array.from(new Uint8Array(hash));
  return bytes.map(b=>b.toString(16).padStart(2,'0')).join('');
}

async function loadConfig(){
  const res = await fetch(KC_CFG_URL, { cache:'no-store' });
  if(!res.ok) throw new Error('config.json introuvable');
  return res.json();
}

function setToken(ttlMinutes){
  const exp = Date.now() + (ttlMinutes*60*1000);
  localStorage.setItem(KC_TOKEN_KEY, JSON.stringify({ exp }));
}
function getToken(){
  try{ const o = JSON.parse(localStorage.getItem(KC_TOKEN_KEY)||''); if(!o) return null; if(Date.now() > o.exp) { localStorage.removeItem(KC_TOKEN_KEY); return null;} return o; }catch(e){ return null }
}
function logout(){ localStorage.removeItem(KC_TOKEN_KEY); location.href = './login.html'; }

function isBlocked(){
  const until = parseInt(localStorage.getItem(KC_BLOCK_KEY)||'0',10);
  return Date.now() < until;
}
function onLoginFail(){
  const count = parseInt(localStorage.getItem(KC_FAIL_KEY)||'0',10)+1;
  localStorage.setItem(KC_FAIL_KEY, String(count));
  if(count >= 5){
    const block = Date.now() + 5*60*1000; // 5 minutes
    localStorage.setItem(KC_BLOCK_KEY, String(block));
  }
}
function onLoginSuccess(){ localStorage.removeItem(KC_FAIL_KEY); localStorage.removeItem(KC_BLOCK_KEY); }

// Guard on admin.html
(async function guard(){
  const isLogin = location.pathname.endsWith('/login.html') || location.href.includes('login.html');
  if(!isLogin){
    const t = getToken();
    if(!t){ location.replace('./login.html'); return; }
    // wire logout
    const btn = document.getElementById('logoutBtn');
    if(btn) btn.addEventListener('click', logout);
  }
})();

// Login handler (on login.html)
(async function loginInit(){
  const form = document.getElementById('loginForm');
  if(!form) return;
  const st = document.getElementById('loginStatus');
  try{
    const cfg = await loadConfig();
    form.addEventListener('submit', async (e)=>{
      e.preventDefault();
      if(isBlocked()){ st.textContent = 'Trop d\'échecs. Réessayez dans quelques minutes.'; return; }
      const pw = (document.getElementById('password').value||'').trim();
      const hex = await sha256Hex(pw);
      if(hex === cfg.passwordHash){
        setToken(cfg.tokenTTLMinutes || 240);
        onLoginSuccess();
        st.textContent = 'Connexion réussie';
        location.href = './admin.html';
      } else {
        onLoginFail();
        st.textContent = 'Mot de passe incorrect';
      }
    });
  }catch(err){ st.textContent = 'Erreur de configuration'; }
})();