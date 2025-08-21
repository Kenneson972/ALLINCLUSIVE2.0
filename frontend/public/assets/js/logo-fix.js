document.addEventListener('DOMContentLoaded', function(){
  try {
    const logos = document.querySelectorAll('img.logo-image');
    logos.forEach(function(img){
      // Always enforce transparent rendering first
      img.style.background = 'transparent';
      img.style.mixBlendMode = 'lighten';
      img.style.boxShadow = 'none';
      // If known opaque PNGs are used, swap to a transparent SVG fallback to guarantee no rectangle
      const needsFallback = /IMG_9175\.png|logo\.png/i.test(img.src);
      if (needsFallback) {
        const svg = '<svg xmlns="http://www.w3.org/2000/svg" width="180" height="50" viewBox="0 0 360 100"><rect width="360" height="100" fill="none"/><text x="50%" y="58%" text-anchor="middle" font-family="Poppins,Segoe UI,Arial,sans-serif" font-size="46" font-weight="700" fill="#ffffff" letter-spacing="1">KhanelConcept</text></svg>';
        const dataUrl = 'data:image/svg+xml;utf8,' + encodeURIComponent(svg);
        img.dataset.orig = img.src;
        img.src = dataUrl;
        img.style.mixBlendMode = 'normal';
      }
    });
  } catch(e) {}
});