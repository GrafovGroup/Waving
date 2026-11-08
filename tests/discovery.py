from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, parse_qs

root=Path(__file__).resolve().parents[1]/'dist'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self, tag, attrs):
  a=dict(attrs)
  if tag=='a':self.links.append(a)
  if 'id' in a:self.ids.add(a['id'])

cases=[('/flags/canada/','Buy Flags',None),('/flags/corporate/','Custom Flags',None),('/flag-rentals/temporary-flagpoles/','Flagpole Rental',None),('/flagpole-installation/commercial/','Flagpole Installation',None),('/flagpole-rope-replacement/','Flagpole Repair',None),('/locations/quebec/montreal/',None,'Montreal')]
for prefix in ['', '/fr']:
 for route,need,city in cases:
  page=Page();page.feed((root/(prefix+route).lstrip('/')/'index.html').read_text())
  quote=[a['href'] for a in page.links if a.get('href','').startswith(prefix+'/quote/?')]
  assert quote,route
  context=parse_qs(urlsplit(quote[0]).query)
  assert context.get('need',[None])[0]==need,(route,context)
  assert context.get('city',[None])[0]==city,(route,context)
  assert context.get('topic'),route
  assert any(a.get('href')==prefix+'/' for a in page.links)
 quote_page=Page();quote_page.feed((root/(prefix+'/quote/').lstrip('/')/'index.html').read_text())
 assert 'quote-form' in quote_page.ids
 assert any(a.get('href')=='#quote-form' for a in quote_page.links)
 assert not any(a.get('href')==prefix+'/quote/' for a in quote_page.links if a.get('class')!='language-link')
print('PASS: product/service/city quote context in both languages; quote-page calls to action keep existing entries in place.')

# Every service CTA must preserve the service selected by the visitor.
for prefix in ['', '/fr']:
 for route,need in [('flag-replacement','Flag Replacement'),('flagpole-maintenance','Commercial Flag Service'),('half-mast-service','Commercial Flag Service'),('flagpole-rope-replacement','Flagpole Repair')]:
  page=Page();page.feed((root/(prefix+'/'+route+'/').lstrip('/')/'index.html').read_text())
  ctas=[a for a in page.links if 'button' in a.get('class','') and a.get('href','').startswith(prefix+'/quote/?')]
  assert len(ctas)>=3,route
  assert all(parse_qs(urlsplit(a['href']).query).get('need')==[need] for a in ctas),(route,ctas)
 rental=Page();rental.feed((root/(prefix+'/flag-rentals/').lstrip('/')/'index.html').read_text())
 packages=[parse_qs(urlsplit(a['href']).query) for a in rental.links if 'package=' in a.get('href','')]
 assert {p['package'][0] for p in packages}=={'flag-only','display-system','event-service'}
 assert all(p.get('topic') and p.get('need') for p in packages)
 catalogue=Page();catalogue.feed((root/(prefix+'/catalogue/').lstrip('/')/'index.html').read_text())
 assert {'catalogue-grid','catalogue-search','catalogue-status','catalogue-empty','catalogue-reset'}<=catalogue.ids
print('PASS: rental package context, catalogue controls and matching service CTA types in English and French.')
