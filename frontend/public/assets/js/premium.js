/* Premium Shared Script - KhanelConcept */
(function(){
  // Mobile nav toggle
  window.toggleMobileNav = function(){
    var nav = document.getElementById('mainNavigation');
    if (!nav) return; 
    nav.classList.toggle('mobile-open');
  };

  // Mark active link
  function markActive(){
    try {
      var current = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
      document.querySelectorAll('nav a').forEach(function(a){
        var href = (a.getAttribute('href') || '').toLowerCase();
        if (href === current) { a.classList.add('active'); a.setAttribute('aria-current','page'); }
      });
    } catch (e) {}
  }

  // Init video for iOS autoplay quirks
  function initBackgroundVideo(){
    var v = document.getElementById('backgroundVideo') || document.getElementById('bgVideo');
    if (!v) return;
    v.muted = true; v.setAttribute('muted',''); v.setAttribute('playsinline',''); v.setAttribute('webkit-playsinline','');
    function tryPlay(){ var p = v.play && v.play(); if (p && typeof p.catch === 'function') { p.catch(function(){}); } }
    tryPlay();
    window.addEventListener('touchstart', function(){ tryPlay(); }, { once:true, passive:true });
  }

  // Animate in elements
  function initAnimations(){
    var els = document.querySelectorAll('.fade-in-up');
    if (!els.length) return;
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){ if (e.isIntersecting) { e.target.style.animationPlayState = 'running'; } });
    }, { threshold: 0.1 });
    els.forEach(function(el){ io.observe(el); });
  }

  document.addEventListener('DOMContentLoaded', function(){
    markActive();
    initBackgroundVideo();
    initAnimations();
  });
})();