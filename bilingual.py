"""Build complete French documents from reviewed, versioned text translations."""
from html.parser import HTMLParser
from pathlib import Path
import html,json,re
ROOT=Path(__file__).parent
sources=json.loads((ROOT/'i18n/source.json').read_text())
def key(s): return re.sub(r'\s+',' ',s.replace(' | Waving.ca','')).strip().rstrip('.').casefold()
rows=dict(line.rstrip('\n').split('\t',1) for line in (ROOT/'i18n/fr.tsv').read_text().splitlines() if line)
for i,city in [(915,'Calgary'),(973,'Vancouver'),(1078,'Ottawa')]: rows[str(i)]=f'À {city} : drapeaux et'
for i,s in enumerate(sources):
 if str(i) not in rows:
  m=re.match(r'For a request in (.*?), include your postal code',s)
  if m:
   city={'Quebec City':'Québec','Montreal':'Montréal'}.get(m[1],m[1])
   rows[str(i)]=f'Pour une demande à {city}, indiquez votre code postal, le type de projet et les dates souhaitées. Appuyez-vous sur les renseignements régionaux ci-dessus pour préciser l’accès, la livraison et les besoins en drapeaux'
missing=[(i,s) for i,s in enumerate(sources) if str(i) not in rows]
if missing: raise ValueError(f'Missing translations: {missing}')
translations={key(s):rows[str(i)] for i,s in enumerate(sources)}
translations.update({'info@waving.ca':'info@waving.ca','accessibility features and contact options for the waving.ca website':'Fonctions d’accessibilité et moyens de communication du site Waving.ca','how the waving.ca website handles quote information and contact details':'Comment le site Waving.ca traite les renseignements des demandes de soumission et les coordonnées', 'home':'Accueil','english':'English','français':'Français'})
translations.update({key(k):v for k,v in json.loads((ROOT/'i18n/improvements.json').read_text()).items()})
# Owner-confirmed names and postal lines remain exact in both languages.
identity_config=json.loads((ROOT/'site-config.json').read_text())
mailing=identity_config['mailingAddress']
for line in [identity_config['brand'],identity_config['legalOperator'],mailing['streetAddress'],*mailing['streetAddress'].split(', ',1),mailing['addressLocality']+', '+mailing['addressRegion'],'Canada '+mailing['postalCode']]:
 translations[key(line)]=line
translations.update({key(identity_config['brand']+' is operated by '+identity_config['legalOperator']):identity_config['brand']+' est exploitée par '+identity_config['legalOperator'],key('Mailing address'):'Adresse postale',key('Company information'):'Renseignements sur l’entreprise',key('Website operator'):'Exploitant du site Web'})
def tr(s):
 if not s.strip(): return s
 k=key(s)
 if not re.search('[a-zA-ZÀ-ÿ]',s) and k not in translations:return s
 if k not in translations: raise ValueError(f'Untranslated text: {s!r}')
 target=translations[k]
 core=s.strip().removesuffix(' | Waving.ca')
 if core.isupper(): target=target.upper()
 elif target.isupper() and len(target)>4: target=target.capitalize()
 if core.endswith('.') and not target.endswith('.'): target+='.'
 if s.strip().endswith(' | Waving.ca'): target+=' | Waving.ca'
 return s[:len(s)-len(s.lstrip())]+target+s[len(s.rstrip()):]
def local_url(s):
 return '/fr'+s if s.startswith('/') and not s.startswith(('/assets/','/favicon','/fr/','//')) else s
class FrenchHTML(HTMLParser):
 def __init__(self): super().__init__(convert_charrefs=True);self.out=[];self.stack=[];self.schema=False
 def handle_decl(self,d): self.out.append('<!'+d+'>')
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.stack.append(tag) if tag not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'] else None
  if tag=='html':a['lang']='fr-CA'
  for k in ['alt','aria-label','placeholder','title']:
   if a.get(k): a[k]=tr(a[k])
  if tag=='meta' and (a.get('name')=='description' or a.get('property') in ['og:title','og:description','og:image:alt']): a['content']=tr(a['content'])
  if tag=='meta' and a.get('property')=='og:locale':a['content']='fr_CA'
  if tag=='meta' and a.get('property')=='og:locale:alternate':a['content']='en_CA'
  if tag=='meta' and a.get('property')=='og:url':a['content']=self.origin+'/fr'+a['content'][len(self.origin):]
  if tag=='link' and a.get('rel')=='canonical':a['href']=self.origin+'/fr'+a['href'][len(self.origin):]
  if a.get('href') and tag=='a' and a.get('class')!='language-link':a['href']=local_url(a['href'])
  if tag=='form' and a.get('action'):a['action']=local_url(a['action'])
  if a.get('data-search'):a['data-search']+=' '+tr(a.get('data-search').split(' ')[0]) if key(a.get('data-search').split(' ')[0]) in translations else ''
  self.schema=tag=='script' and a.get('type')=='application/ld+json' if tag=='script' else self.schema
  self.out.append('<'+tag+''.join(' '+k+(('="'+html.escape(v,quote=True)+'"') if v is not None else '') for k,v in a.items())+'>')
 def handle_endtag(self,t):
  self.out.append('</'+t+'>')
  if self.stack and self.stack[-1]==t:self.stack.pop()
  if t=='script':self.schema=False
 def handle_data(self,d):
  if self.schema:
   obj=json.loads(d)
   for item in obj['@graph']:
    if item['@type'] in ('Organization','WebSite'):continue
    for k in ['name','description']:
     if k in item:item[k]=tr(item[k])
    if 'url' in item:item['url']=self.origin+'/fr'+item['url'][len(self.origin):]
    if '@id' in item:item['@id']=self.origin+'/fr'+item['@id'][len(self.origin):]
    if 'breadcrumb' in item:item['breadcrumb']['@id']=self.origin+'/fr'+item['breadcrumb']['@id'][len(self.origin):]
    item['inLanguage']='fr-CA'
    for crumb in item.get('itemListElement',[]):
     crumb['name']=tr(crumb['name']);crumb['item']=self.origin+'/fr'+crumb['item'][len(self.origin):]
   self.out.append(json.dumps(obj,ensure_ascii=False));return
  self.out.append(d if self.stack and self.stack[-1] in ['script','style'] else html.escape(tr(d),quote=False))
 def handle_comment(self,d): self.out.append('<!--'+d+'-->')
def documents(document,path,origin):
 alt=''.join(f'<link rel="alternate" hreflang="{lang}" href="{origin}{prefix}{path}">' for lang,prefix in [('en-CA',''),('fr-CA','/fr'),('x-default','')])
 document=document.replace('</head>',alt+'</head>')
 parser=FrenchHTML();parser.origin=origin;parser.feed(document)
 french=''.join(parser.out).replace('<script defer src="/assets/site.js">','<script defer src="/assets/i18n-fr.js"></script><script defer src="/assets/site.js">')
 # Insert switches after translation so their language labels and target routes stay exact.
 def switch(doc,fr):
  links=f'<div class="language-switch" role="group" aria-label="{"Langue du site" if fr else "Website language"}"><a class="language-link" href="{path}" lang="en" hreflang="en-CA"{(" aria-current=\"true\"" if not fr else "")}>EN</a><span aria-hidden="true">/</span><a class="language-link" href="/fr{path}" lang="fr" hreflang="fr-CA"{(" aria-current=\"true\"" if fr else "")}>FR</a></div>'
  return doc.replace('<div class="header-right">','<div class="header-right">'+links)
 return switch(document,False),switch(french,True)

def runtime():
 values=dict(translations)
 for line in (ROOT/'i18n/runtime.tsv').read_text().splitlines():
  a,b=line.split('\t',1);values[key(a)]=b.rstrip('.')
 phone=json.loads((ROOT/'site-config.json').read_text())['phone']
 values={key(k.replace('(833) 696-9996',phone)):v.replace('(833) 696-9996',phone) for k,v in values.items()}
 (ROOT/'dist/assets/i18n-fr.js').write_text('window.WAVING_FR='+json.dumps(values,ensure_ascii=False)+';\n'+(ROOT/'i18n/runtime.js').read_text())
