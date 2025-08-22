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

  document.addEventListener('DOMContentLoaded', function(){
    markActive(); initSmooth(); initVideo();
    // Reveal animation
    var els = document.querySelectorAll('.fade-in-up');
    var io = new IntersectionObserver(function(entries){ entries.forEach(function(e){ if(e.isIntersecting){ e.target.style.animationPlayState='running'; } }); }, { threshold: 0.1 });
    els.forEach(function(el){ io.observe(el); });
  });
})();