/* Robust image paths + placeholder fallback */
function attachImageFallbacks(scope){
  const root = scope || document;
  root.querySelectorAll('img').forEach(img=>{
    img.addEventListener('error', ()=>{
      img.src = '../images/placeholder_villa.webp';
      img.closest('.card')?.querySelector('.badge')?.classList.add('show');
    }, { once:true });
  });
}