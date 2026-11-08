const isFrench=document.documentElement.lang==='fr-CA';
const toggle=document.querySelector('.menu-toggle'),nav=document.querySelector('#navigation');
function setMenu(open,restoreFocus=false){
 if(!toggle||!nav)return;
 toggle.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open);
 toggle.textContent=open?(isFrench?'FERMER':'CLOSE'):'MENU';
 if(!open)nav.querySelectorAll('details[open]').forEach(d=>d.open=false);
 if(restoreFocus)toggle.focus();
}
toggle?.addEventListener('click',()=>setMenu(toggle.getAttribute('aria-expanded')!=='true'));
nav?.addEventListener('click',e=>{if(e.target.closest('a'))setMenu(false)});
document.addEventListener('click',e=>{if(!e.target.closest('.site-header'))setMenu(false)});
window.matchMedia('(max-width:760px)').addEventListener('change',()=>setMenu(false));
document.querySelectorAll('#navigation a').forEach(a=>{if(location.pathname===a.pathname)a.setAttribute('aria-current','page')});
const fold=s=>s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
const search=document.querySelector('#location-search');search?.addEventListener('input',()=>{let shown=0;const q=fold(search.value.trim());document.querySelectorAll('.location-group[data-search]').forEach(g=>{g.hidden=!fold(g.dataset.search+' '+g.textContent).includes(q);if(!g.hidden)shown++});document.querySelector('#location-count').textContent=isFrench?`${shown} région${shown===1?'':'s'} correspondante${shown===1?'':'s'}.`:`${shown} matching ${shown===1?'region':'regions'}.`;document.querySelector('#no-locations').hidden=shown!==0});document.querySelectorAll('a[href^="tel:"]').forEach(a=>a.addEventListener('click',()=>window.dispatchEvent(new CustomEvent('waving:analytics',{detail:{event:'phone_click'}}))));
const menus=[...document.querySelectorAll('.nav-group')];menus.forEach(m=>m.addEventListener('toggle',()=>{if(m.open)menus.forEach(other=>{if(other!==m)other.open=false})}));document.addEventListener('click',e=>{if(!e.target.closest('.nav-group'))menus.forEach(m=>m.open=false)});document.addEventListener('keydown',e=>{if(e.key!=='Escape')return;if(nav?.classList.contains('open')){setMenu(false,true);return}menus.forEach(m=>{if(m.open){m.open=false;m.querySelector('summary').focus()}})});

document.querySelectorAll('.language-link').forEach(a=>{a.search=location.search; a.hash=location.hash;});
