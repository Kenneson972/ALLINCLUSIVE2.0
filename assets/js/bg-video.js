(function(){
  if(document.querySelector('.video-background')) return;
  var poster='images/hero-poster.jpg';
  var webm='https://res.cloudinary.com/ddulasmtz/video/upload/v1752950782/background-video.webm';
  var mp4 ='https://res.cloudinary.com/ddulasmtz/video/upload/v1752950782/background-video.mp4';
  var wrap=document.createElement('div');wrap.className='video-background';
  var v=document.createElement('video');
  v.autoplay=true;v.loop=true;v.muted=true;v.playsInline=true;v.setAttribute('poster',poster);
  var s1=document.createElement('source');s1.src=webm;s1.type='video/webm';
  var s2=document.createElement('source');s2.src=mp4;s2.type='video/mp4';
  v.appendChild(s1);v.appendChild(s2);
  wrap.appendChild(v);
  var o=document.createElement('div');o.className='video-overlay';wrap.appendChild(o);
  var b=document.body;if(b.firstChild)b.insertBefore(wrap,b.firstChild);else b.appendChild(wrap);
})();