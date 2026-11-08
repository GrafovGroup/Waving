"""Validate crawl policy and connected metadata on the generated bilingual site."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json
import xml.etree.ElementTree as ET

root=Path(__file__).resolve().parents[1]/'dist'
origin=json.loads((root.parent/'site-config.json').read_text())['origin'].rstrip('/')

class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.meta={};self.canonical=None;self.lang=None;self.in_schema=False;self.schema_text=''
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='html':self.lang=a.get('lang')
  if tag=='meta':self.meta[a.get('name') or a.get('property')]=a.get('content')
  if tag=='link' and a.get('rel')=='canonical':self.canonical=a['href']
  if tag=='script':self.in_schema=a.get('type')=='application/ld+json'
 def handle_endtag(self,tag):
  if tag=='script':self.in_schema=False
 def handle_data(self,text):
  if self.in_schema:self.schema_text+=text

sitemap=ET.parse(root/'sitemap.xml')
urls=[loc.text for loc in sitemap.findall('.//{*}loc')]
assert len(urls)==len(set(urls)), 'Duplicate sitemap URLs'
indexable=set()
count=0
for path in root.rglob('*.html'):
 page=Page();page.feed(path.read_text())
 graph=json.loads(page.schema_text)['@graph']
 nodes={n['@id']:n for n in graph}
 assert len(nodes)==len(graph),path
 org=nodes[origin+'/#organization'];website=nodes[origin+'/#website']
 assert org['logo']['url']==origin+'/assets/waving-ca-wave-lettering.webp',path
 assert website['url']==origin+'/' and website['publisher']['@id'] in nodes,path
 webpage=nodes[page.canonical+'#webpage']
 assert webpage['url']==page.canonical and webpage['inLanguage']==page.lang,path
 assert webpage['isPartOf']['@id'] in nodes and webpage['about']['@id'] in nodes,path
 if 'breadcrumb' in webpage:
  crumbs=nodes[webpage['breadcrumb']['@id']]['itemListElement']
  assert crumbs[-1]['item']==page.canonical,path
  assert all(('/fr/' in c['item'])==(page.lang=='fr-CA') for c in crumbs),path
 assert page.meta['og:url']==page.canonical,path
 assert page.meta['og:locale']==page.lang.replace('-','_'),path
 assert page.meta['og:image:alt'] and page.meta['twitter:card']=='summary_large_image',path
 image=urlsplit(page.meta['og:image'])
 assert image.netloc==urlsplit(origin).netloc and (root/image.path.lstrip('/')).is_file(),path
 if 'noindex' not in page.meta['robots']:indexable.add(page.canonical)
 count+=1
assert set(urls)==indexable, 'Sitemap must contain exactly the indexable canonical pages'
assert all('/search/' not in url and '/404/' not in url for url in urls)
print(f'PASS: {count} pages with localized, connected metadata; {len(urls)} indexable sitemap URLs; search and error pages excluded.')
