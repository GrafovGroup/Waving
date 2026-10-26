from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
root=Path(__file__).parent/'dist'
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.ids=set();self.h1=0;self.title=False;self.desc=False;self.robots=False;self.noindex=False;self.canonical=False;self.schema=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id'in a:self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True
  if tag=='meta' and a.get('name')=='description':self.desc=bool(a.get('content'))
  if tag=='meta' and a.get('name')=='robots':self.robots=bool(a.get('content'));self.noindex='noindex'in a.get('content','')
  if tag=='link' and a.get('rel')=='canonical':self.canonical=True
  if tag=='script' and a.get('type')=='application/ld+json':self.schema=True
  for k in ['href','src']:
   if k in a:self.refs.append(a[k])
parsed={}
for p in root.rglob('*.html'):
 h=Parser();h.feed(p.read_text());parsed[p]=h
errors=[]
for p,h in parsed.items():
 if h.h1!=1:errors.append(f'{p}: {h.h1} H1s')
 if not all([h.title,h.desc,h.robots,h.canonical,h.schema]):errors.append(f'{p}: metadata missing')
 if h.noindex != ('404' in p.parts or p.name=='404.html'):errors.append(f'{p}: unexpected indexing directive')
 for ref in h.refs:
  url=urlsplit(ref)
  if url.scheme or url.netloc:continue
  path=unquote(url.path)
  target=(root/path.lstrip('/')) if path.startswith('/') else p.parent/path
  if not path:target=p
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'{p.relative_to(root)}: broken {ref}')
  elif url.fragment and target in parsed and unquote(url.fragment) not in parsed[target].ids:errors.append(f'{p.relative_to(root)}: missing anchor {ref}')
result={'html_files':len(parsed),'internal_links_assets_anchors':'pass' if not errors else 'fail','metadata':'checked','errors':errors}
print(json.dumps(result,indent=2))
raise SystemExit(bool(errors))
