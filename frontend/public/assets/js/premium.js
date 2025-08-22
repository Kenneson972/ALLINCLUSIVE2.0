(function(){
  // Mobile toggle
  window.toggleMobileNav = function(){
    var nav = document.getElementById('mainNavigation');
    if (!nav) return; nav.classList.toggle('mobile-open');
  };

  // Mark active link
  function markActive(){
    try{ var current=(location.pathname.split('/').pop()||'index.html').toLowerCase();
      document.querySelectorAll('nav a').forEach(function(a){ var href=(a.getAttribute('href')||'').toLowerCase(); if(href===current){ a.classList.add('active'); a.setAttribute('aria-current','page'); }});
    }catch(e){}
  }

  // Smooth scroll for internal anchors
  function initSmooth(){
    document.querySelectorAll('a[href^="#"]').forEach(function(a){
      a.addEventListener('click', function(e){
        var id = this.getAttribute('href').slice(1);
        var el = document.getElementById(id);
        if(el){ e.preventDefault(); window.scrollTo({ top: el.getBoundingClientRect().top + window.pageYOffset - 90, behavior: 'smooth' }); }
      });
    });
  }

  // iOS video autoplay helper
  function initVideo(){
    var v = document.getElementById('backgroundVideo') || document.getElementById('bgVideo') || document.querySelector('.video-background video');
    if(!v) return; v.muted=true; v.setAttribute('muted',''); v.setAttribute('playsinline',''); v.setAttribute('webkit-playsinline','');
    var play=function(){ var p=v.play&&v.play(); if(p&&p.catch) p.catch(function(){}); };
    play(); window.addEventListener('touchstart', function(){ play(); }, {once:true, passive:true});
  }

  // 3D micro-parallax for cards (desktop only)
  function initParallax(){
    if (window.matchMedia('(pointer: coarse)').matches) return; // skip on touch-only
    document.querySelectorAll('.card').forEach(function(card){
      var rect;
      function onMove(e){
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        card.style.setProperty('--rx', (y * -2)+'deg');
        card.style.setProperty('--ry', (x * 2)+'deg');
        card.style.setProperty('--shift', (x * 6)+'px');
        card.style.setProperty('--ty', (y * 6)+'px');
        card.style.setProperty('--scale', '1.01');
      }
      function onEnter(){ rect = card.getBoundingClientRect(); }
      function onLeave(){ card.style.setProperty('--rx','0deg'); card.style.setProperty('--ry','0deg'); card.style.setProperty('--shift','0px'); card.style.setProperty('--ty','0px'); card.style.setProperty('--scale','1'); }
      card.addEventListener('mouseenter', onEnter);
      card.addEventListener('mousemove', onMove);
      card.addEventListener('mouseleave', onLeave);
    });
  }

  document.addEventListener('DOMContentLoaded', function(){
    markActive(); initSmooth(); initVideo(); initParallax();
    // Reveal animation
    var els = document.querySelectorAll('.fade-in-up');
    var io = new IntersectionObserver(function(entries){ entries.forEach(function(e){ if(e.isIntersecting){ e.target.style.animationPlayState='running'; } }); }, { threshold: 0.1 });
    els.forEach(function(el){ io.observe(el); });
  });
})();