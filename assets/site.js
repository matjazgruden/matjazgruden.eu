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
(function(){
  // full-text search
  var list=document.querySelector('.results'); if(!list) return;
  var form=document.querySelector('.fts'), input=document.getElementById('fq'), count=document.querySelector('.count');
  var M=JSON.parse(list.dataset.msg), lang=list.dataset.lang, base=list.dataset.index.replace(/assets\/search-\w+\.json$/,'');
  var EN=['January','February','March','April','May','June','July','August','September','October','November','December'];
  var SL=['januarja','februarja','marca','aprila','maja','junija','julija','avgusta','septembra','oktobra','novembra','decembra'];
  var SLN=['januar','februar','marec','april','maj','junij','julij','avgust','september','oktober','november','december'];
  function fdate(d){if(!d) return ''; var p=d.split('-');
    if(p.length===2) return (lang==='sl'?SLN:EN)[+p[1]-1]+' '+p[0];
    return lang==='sl'? (+p[2])+'. '+SL[+p[1]-1]+' '+p[0] : (+p[2])+' '+EN[+p[1]-1]+' '+p[0];}
  var MARKS=/[̀-ͯ]/g;
  function fold(c){return c.normalize('NFD').replace(MARKS,'').toLowerCase().replace(/[‘’]/g,"'").replace(/[“”„]/g,'"')}
  function norm(s){var out='',map=[];for(var i=0;i<s.length;i++){var f=fold(s[i]);for(var j=0;j<f.length;j++){out+=f[j];map.push(i)}}return {s:out,map:map}}
  var docs=null;
  function load(cb){ if(docs) return cb();
    count.textContent=M.loading;
    fetch(list.dataset.index).then(function(r){return r.json()}).then(function(d){
      docs=d.map(function(x){var b=norm(x[4]);return {title:x[0],url:x[1],date:x[2],k:x[3],text:x[4],nt:b.s,map:b.map,ntitle:fold(x[0])}});cb();
    }).catch(function(){count.textContent=''});
  }
  function terms(q){var t=[],re=/"([^"]+)"|(\S+)/g,m;q=fold(q);while((m=re.exec(q))){var w=(m[1]||m[2]).replace(/^[^\w"']+|[^\w"']+$/g,'');if(w.length>1||m[1]) t.push(w)}return t}
  var LETTER=/[\p{L}\p{N}]/u;
  function hits(s,t){var out=[],i=0;while((i=s.indexOf(t,i))>-1){if(i===0||!LETTER.test(s[i-1])) out.push(i);i+=t.length}return out}
  function esc(s){return s.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function snippet(d,ts){
    var first=-1,ph=ts.length>1?hits(d.nt,ts.join(' ')):[];
    if(ph.length) first=ph[0]; else ts.forEach(function(t){var h=hits(d.nt,t);if(h.length&&(first<0||h[0]<first)) first=h[0]});
    if(first<0) return esc(d.text.slice(0,200))+'…';
    var a=Math.max(0,d.map[first]-90),b=Math.min(d.text.length,d.map[first]+180);
    a=d.text.lastIndexOf(' ',a)+1; var seg=d.text.slice(a,b), nseg=norm(seg), html='', last=0, hl=[];
    ts.forEach(function(t){hits(nseg.s,t).forEach(function(i){hl.push([nseg.map[i],nseg.map[i+t.length-1]+1])})});
    hl.sort(function(x,y){return x[0]-y[0]});
    hl.forEach(function(h){if(h[0]<last) return; html+=esc(seg.slice(last,h[0]))+'<mark>'+esc(seg.slice(h[0],h[1]))+'</mark>'; last=h[1]});
    html+=esc(seg.slice(last)); return (a>0?'… ':'')+html+(b<d.text.length?' …':'');
  }
  function run(q){
    var ts=terms(q); list.innerHTML='';
    if(!ts.length){count.textContent='';return}
    load(function(){
      var res=[];
      docs.forEach(function(d){var score=0;for(var i=0;i<ts.length;i++){var t=ts[i],n=hits(d.nt,t).length,inT=hits(d.ntitle,t).length>0;
          if(!n&&!inT) return; score+=Math.min(n,20)+(inT?15:0)}
        if(ts.length>1){var ph=ts.join(' '); score+=5*Math.min(hits(d.nt,ph).length,10)+(hits(d.ntitle,ph).length?30:0)}
        res.push({d:d,s:score})});
      res.sort(function(a,b){return b.s-a.s||(a.d.date<b.d.date?1:-1)});
      var n=res.length;
      count.textContent=n?n+' '+(n===1?M.one:M.many)+(n>100?'. '+M.more:''):M.none;
      list.innerHTML=res.slice(0,100).map(function(r){var d=r.d;
        return '<li><a href="'+base+d.url+'"><span class="t">'+esc(d.title)+'</span></a><time datetime="'+d.date+'">'+fdate(d.date)+'</time><p>'+snippet(d,ts)+'</p></li>'}).join('');
    });
  }
  var q0=new URLSearchParams(location.search).get('q')||''; input.value=q0; if(q0) run(q0);
  form.addEventListener('submit',function(e){e.preventDefault();var q=input.value.trim();
    try{history.replaceState(null,'','?q='+encodeURIComponent(q))}catch(_){}
    run(q)});
})();
/* copy-to-clipboard buttons (Follow page) */
(function(){
  document.querySelectorAll('[data-copy]').forEach(function(b){
    b.addEventListener('click',function(){
      var t=b.getAttribute('data-copy'),label=b.textContent;
      function done(){b.textContent=b.getAttribute('data-done')||'Copied';setTimeout(function(){b.textContent=label},1800)}
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,function(){})}
    });
  });
})();
