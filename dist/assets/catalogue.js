(()=>{'use strict';
const grid=document.querySelector('#catalogue-grid');if(!grid)return;
const input=document.querySelector('#catalogue-search'),buttons=[...document.querySelectorAll('[data-catalogue-filter]')],cards=[...grid.children],status=document.querySelector('#catalogue-status'),empty=document.querySelector('#catalogue-empty');
const fr=document.documentElement.lang==='fr-CA',normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
const params=new URLSearchParams(location.search);let category=buttons.some(b=>b.dataset.catalogueFilter===params.get('category'))?params.get('category'):'';
input.value=(params.get('q')||'').slice(0,160);
const searchable=cards.map(card=>normalize(card.querySelector('div').textContent));
function render(updateUrl=true){const words=normalize(input.value.trim()).split(/\s+/).filter(Boolean);let count=0;
 cards.forEach((card,i)=>{card.hidden=!!((category&&card.dataset.category!==category)||!words.every(word=>searchable[i].includes(word)));if(!card.hidden)count++});
 buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.catalogueFilter===category)));
 status.textContent=fr?`${count} famille${count===1?'':'s'} de produits sur ${cards.length}`:`${count} of ${cards.length} product families`;empty.hidden=count!==0;
 if(updateUrl){const url=new URL(location.href);if(input.value.trim())url.searchParams.set('q',input.value.trim());else url.searchParams.delete('q');if(category)url.searchParams.set('category',category);else url.searchParams.delete('category');history.replaceState(null,'',url)}
}
buttons.forEach(button=>button.addEventListener('click',()=>{category=button.dataset.catalogueFilter;render()}));input.addEventListener('input',()=>render());
document.querySelector('#catalogue-reset').addEventListener('click',()=>{category='';input.value='';render();input.focus()});
document.querySelector('.catalogue-toolbar').hidden=false;render(false);
})();
