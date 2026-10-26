from pathlib import Path
from html.parser import HTMLParser
import json
root=Path(__file__).parent/'dist'
origin=json.loads((root.parent/'site-config.json').read_text())['origin'].rstrip('/')
class Page(HTMLParser):
 def __init__(self):super().__init__();self.lang=None;self.canonical=None;self.alternates={};self.links=[];self.scripts=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='html':self.lang=a.get('lang')
  if t=='link' and a.get('rel')=='canonical':self.canonical=a['href']
  if t=='link' and a.get('rel')=='alternate':self.alternates[a['hreflang']]=a['href']
  if t=='a':self.links.append(a)
  if t=='script':self.scripts.append(a.get('src'))
count=0
for p in root.rglob('index.html'):
 if p.relative_to(root).parts[0]=='fr':continue
 route='/'+str(p.parent.relative_to(root)).strip('.')
 if not route.endswith('/'):route+='/'
 q=root/'fr'/p.relative_to(root)
 assert q.exists(),q
 for file,lang,prefix in [(p,'en-CA',''),(q,'fr-CA','/fr')]:
  h=Page();h.feed(file.read_text())
  assert h.lang==lang
  assert h.canonical==origin+prefix+route,(file,h.canonical)
  assert h.alternates=={'en-CA':origin+route,'fr-CA':origin+'/fr'+route,'x-default':origin+route}
  assert len([a for a in h.links if a.get('class')=='language-link'])==2
  if prefix:
   assert '/assets/i18n-fr.js' in h.scripts
   for a in h.links:
    link=a.get('href','')
    if link.startswith('/') and a.get('class')!='language-link':assert link.startswith('/fr/'),(q,link)
 count+=1
print(f'PASS: {count} English/French route pairs, self-canonicals, reciprocal hreflang, matching language switches and French internal navigation.')
