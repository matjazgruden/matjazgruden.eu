(function(){
  // timeline caption
  document.querySelectorAll('.tl').forEach(function(tl){
    var cap=tl.querySelector('.tl-cap'), def=cap.innerHTML;
    function show(m){cap.innerHTML='<b></b><br>';cap.querySelector('b').textContent=m.dataset.t;cap.appendChild(document.createTextNode(m.dataset.d));}
    tl.querySelectorAll('.mk').forEach(function(m){
      m.addEventListener('mouseenter',function(){show(m)});
      m.addEventListener('focus',function(){show(m)});
    });
    tl.addEventListener('mouseleave',function(){cap.innerHTML=def});
  });
  // archive filters
  var arch=document.querySelector('.archive'); if(!arch) return;
  var q=document.getElementById('q'), en=document.getElementById('only-en'), f='all';
  var chips=document.querySelectorAll('.chip'), count=document.querySelector('.count');
  function norm(s){return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')}
  var items=[].slice.call(arch.querySelectorAll('li')).map(function(li){return {li:li,t:norm(li.textContent)}});
  function apply(){
    var s=norm(q.value.trim()), n=0;
    items.forEach(function(it){
      var ok=(f==='all'||it.li.dataset.k===f)&&(!s||it.t.indexOf(s)>-1)&&(!en||!en.checked||it.li.dataset.en==='1');
      it.li.hidden=!ok; if(ok) n++;
    });
    arch.querySelectorAll('.yr').forEach(function(y){y.hidden=!y.querySelector('li:not([hidden])')});
    count.textContent=n+' '+(n===1?count.dataset.one:count.dataset.many);
  }
  chips.forEach(function(c){c.addEventListener('click',function(){
    f=c.dataset.f; chips.forEach(function(x){x.setAttribute('aria-pressed',x===c?'true':'false')}); apply();
  })});
  q.addEventListener('input',apply); if(en) en.addEventListener('change',apply);
  apply();
})();
