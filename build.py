from pathlib import Path
import json, html, re, shutil, hashlib
from urllib.parse import urlencode
from bilingual import tr
from bilingual import documents, runtime
ROOT=Path(__file__).parent
OUT=ROOT/'dist'
CONFIG=json.loads((ROOT/'site-config.json').read_text())
PAGES={}
NOINDEX_PATHS={'/404/','/search/'}
def esc(s): return html.escape(str(s),quote=True)
def link(url,label,cls=''): return f'<a class="{cls}" href="{url}">{label}</a>'
def button(label='GET A QUOTE',need=''): return link('/quote/'+('?need='+need if need else ''),label,'button')
def img(kind='hero',alt='',cls=''): return f'<img class="{cls}" src="/assets/{kind}.webp" alt="{esc(alt)}" width="1536" height="1024" loading="lazy" decoding="async">'
NAV=[('FLAGS','/flags/'),('FLAGPOLES','/flagpoles/'),('RENTALS','/flag-rentals/'),('INSTALLATION','/flagpole-installation/'),('SERVICES','/services/'),('INDUSTRIES','/industries/'),('LOCATIONS','/locations/'),('RESOURCES','/resources/'),('ABOUT','/about/'),('CONTACT','/contact/')]
LOGO='<span class="brand-logo"><img src="/assets/waving-ca-wave-lettering.webp" alt="" width="1983" height="793" decoding="async"></span>'
def header():
 return f'''<a class="skip" href="#main">Skip to content</a><div class="utility"><span>FLAGS. FLAGPOLES. INSTALLATION. SERVICE.</span><a href="tel:+18336969996">(833) 696-9996</a></div><header class="site-header"><div class="header-main"><a class="brand-link" href="/" aria-label="Waving.ca home">{LOGO}</a><div class="header-right"><a class="header-search" href="/search/"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"></circle><path d="m16 16 5 5"></path></svg><span>Search</span></a>{button()}<button class="menu-toggle" aria-expanded="false" aria-controls="navigation">MENU</button></div></div><nav id="navigation" aria-label="Main navigation">{navigation()}</nav></header>'''
def navigation():
 groups=[
  ('FLAGS','/flags/',[('Product catalogue','/catalogue/')]+[(x[1],'/flags/'+x[0]+'/') for x in FLAGS]+[('Parts & accessories','/accessories/')]),
  ('FLAGPOLES','/flagpoles/',[(x[1],'/flagpoles/'+x[0]+'/') for x in POLES]),
  ('RENTALS','/flag-rentals/',[(x[1],'/flag-rentals/'+x[0]+'/') for x in RENTALS]),
  ('INSTALLATION & SERVICE','/services/',[('Flagpole installation','/flagpole-installation/')]+[(x[1],'/'+x[0]+'/') for x in SERVICES]+[('Commercial flag management','/flag-service/'),('Multi-location accounts','/commercial-accounts/'),('Specialist services','/services/specialist/')]),
  ('BUYING GUIDES','/resources/',[('Choosing a flag','/resources/choosing-a-flag/'),('Choosing a flagpole','/resources/choosing-a-flagpole/'),('Installation cost guide','/resources/installation-cost/'),('Planning an event flag rental','/resources/rental-planning/'),('Looking after your flags','/resources/flag-care/'),('Canadian flag etiquette','/resources/flag-etiquette/')]),
  ('WAVING.CA','/about/',[('About Waving.ca','/about/'),('Contact Waving.ca','/contact/'),('Locations','/locations/'),('Industries','/industries/')])
 ]
 result='<a class="mobile-search" href="/search/">Search products &amp; services</a>'
 for title,url,items in groups:
  result+=f'<details class="nav-group"><summary>{title}</summary><div class="mega"><a class="mega-overview" href="{url}">{esc(PAGES[url]["title"])}</a><div>'+''.join(link(u,t) for t,u in items)+'</div></div></details>'
 return result

def business_identity():
 address=CONFIG['mailingAddress']
 lines=address['streetAddress'].split(', ',1)+[address['addressLocality']+', '+address['addressRegion'],'Canada '+address['postalCode']]
 operator=f"{CONFIG['brand']} is operated by {CONFIG['legalOperator']}"
 return '<p class="legal-operator">'+esc(operator)+'</p><address class="business-address"><span class="address-label">Mailing address</span><br>'+'<br>'.join(esc(line) for line in lines)+'</address>'

def footer():
 return f'''<section class="final-cta wrap"><div><p class="eyebrow">LET’S GET STARTED</p><h2>Ready to get waving?</h2><p>Tell us what you need and where you need it.</p></div>{button()}</section><footer><div class="wrap footer-grid"><div><a class="brand-link" href="/" aria-label="Waving.ca home">{LOGO}</a><p>Flags for a place.<br>Service for the long run.</p><a class="phone" href="tel:+18336969996">(833) 696-9996</a><p><a href="mailto:{esc(CONFIG['enquiryEmail'])}">{esc(CONFIG['enquiryEmail'])}</a></p></div><div><h3>EXPLORE</h3>{''.join(link(u,t) for t,u in NAV[:5])}</div><div><h3>WAVING.CA</h3>{''.join(link(u,t) for t,u in NAV[5:])}</div><div><h3>LET’S TALK</h3><p>One flag or a whole portfolio.<br>Start with what you have in mind.</p>{button('REQUEST A QUOTE')}</div></div><div class="wrap footer-bottom"><span>© {2026} Waving.ca. Keep Canada waving.</span><div><a href="/privacy/">PRIVACY</a><a href="/accessibility/">ACCESSIBILITY</a></div></div></footer><div class="mobile-actions"><a href="tel:+18336969996">CALL</a><a href="/quote/">GET A QUOTE</a></div>'''
def add(path,title,description,body,kind='WebPage'):
 PAGES[path]={'title':title,'description':description,'body':body,'kind':kind}
def section_head(kicker,title,description=''):
 return f'<div class="section-head"><p class="eyebrow">{kicker}</p><h2>{title}</h2>'+ (f'<p>{description}</p>' if description else '')+'</div>'
def cards(items,cls=''):
 return '<div class="cards '+cls+'">'+''.join(f'<a class="card" href="{u}"><span class="card-index">{i+1:02d}</span><h3>{t}</h3><p>{d}</p><span class="text-link">EXPLORE</span></a>' for i,(t,u,d) in enumerate(items))+'</div>'
def split(kicker,title,text,image='hero',alt='Flags outside a modern commercial property',extra=''):
 return f'<section class="wrap split"><div>{section_head(kicker,title)}<p>{text}</p>{extra}</div><div class="image-frame">{img(image,alt)}</div></section>'
def hero(kicker,title,desc,image='hero',alt=None):
 if alt is None: alt={'hero':'Flags flying outside a modern commercial building','event':'Portable flags arranged across an outdoor event plaza','hardware':'Aluminum flagpole cleat with secured rope and hardware'}[image]
 return f'<section class="page-hero wrap"><div><p class="eyebrow">{kicker}</p><h1>{title}</h1><p class="lead">{desc}</p>{button()}</div><div class="image-frame">{img(image,alt).replace('loading="lazy"','loading="eager"')}</div></section>'
def faq(items): return '<section class="wrap faq"><div>'+section_head('GOOD TO KNOW','A few useful answers.')+'</div><div>'+''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in items)+'</div></section>'
def steps(items): return '<ol class="steps">'+''.join(f'<li><span>{i+1:02d}</span><h3>{a}</h3><p>{b}</p></li>' for i,(a,b) in enumerate(items))+'</ol>'
HOME='''<section class="home-hero"><div class="hero-photo"><img src="/assets/hero.webp" alt="Canadian and neutral flags flying beside a contemporary commercial property" width="1536" height="1024" fetchpriority="high"></div><div class="hero-content wrap"><p class="eyebrow">FOR THE PLACES THAT BRING US TOGETHER</p><h1>CANADA’S<br>FLAG &amp;<br>FLAGPOLE<br>COMPANY<span>.</span></h1><p>Flags, flagpoles, rentals, installation and ongoing service for businesses, events, institutions and properties across Canada.</p><div class="actions"><a class="button" href="/quote/">GET A QUOTE</a><a class="button outline light" href="/flags/">EXPLORE FLAGS</a></div><div class="hero-caption"><span>FROM ONE FLAG</span><span>TO EVERY LOCATION.</span></div></div></section>'''
HOME+='<section class="service-finder wrap"><div class="finder-heading"><div><p class="eyebrow">WHAT DO YOU NEED?</p><h2>Start with your project.</h2></div>'+link('/search/','Search products &amp; services','text-link')+'</div><div class="service-choices">'+''.join(f'<a href="{u}"><span class="choice-number" aria-hidden="true">{i+1:02d}</span><div><h3>{t}</h3><p>{d}</p></div><span class="choice-arrow" aria-hidden="true">↗</span></a>' for i,(t,u,d) in enumerate([('Buy flags','/flags/','Canadian, provincial, international and more.'),('Create custom flags','/custom-flags/','Your artwork, colours and brand in motion.'),('Rent for an event','/flag-rentals/','Flags, portable poles and event setup.'),('Install a flagpole','/flagpole-installation/','Plan a new display for your property.'),('Repair a flagpole','/flagpole-repair/','Help with ropes, hardware and worn parts.'),('Manage your displays','/flag-service/','Replacement and care for one site or many.')]))+'</div></section>'

HOME+='<section class="wrap section"><div class="section-title-row">'+section_head('SOMETHING WORTH FLYING','For every place.<br>For every purpose.')+link('/flags/','EXPLORE ALL FLAGS','text-link')+'</div><div class="feature-grid"><a class="feature-tile" href="/flags/canada/">'+img('hero','Canadian flag flying from an aluminum flagpole')+'<div><p class="eyebrow">A FAMILIAR SYMBOL. A FRESH START.</p><h3>Canadian flags</h3></div></a><a class="feature-tile" href="/custom-flags/">'+img('event','Navy and white flags at an outdoor event')+'<div><p class="eyebrow">MAKE YOUR MARK</p><h3>Your brand. In motion.</h3></div></a></div><div class="category-links">'+''.join(link('/flags/'+s+'/',t) for s,t in [('provincial','PROVINCIAL & TERRITORIAL'),('international','INTERNATIONAL'),('corporate','CORPORATE'),('municipal','MUNICIPAL'),('indigenous','INDIGENOUS'),('event','EVENT'),('sports','SPORTS'),('feather','FEATHER'),('banner','BANNER')])+'</div></section>'
HOME+=split('A STRONG FOUNDATION','The right pole.<br>The right presence.','From a residential entrance to a multi-pole commercial display, start with a flagpole suited to the setting, flag size and exposure. We help bring the pieces together.','hardware','Aluminum flagpole with cleat and secured halyard',link('/flagpoles/','EXPLORE FLAGPOLES','button navy'))
HOME+='<section class="rental-band"><div class="rental-image">'+img('event','Portable event flags arranged across an outdoor plaza')+'</div><div class="rental-copy"><p class="eyebrow">BIG OCCASION. SHORT-TERM SOLUTION.</p><h2>Need flags<br>temporarily?</h2><p>Set the scene for a conference, ceremony, festival or film production. Explore flags, portable poles and coordinated event installation.</p><div class="pill-row"><span>EVENTS</span><span>FESTIVALS</span><span>CEREMONIES</span><span>FILM</span></div>'+button('GET RENTAL PRICING','Flag%20Rental')+'</div></section>'
HOME+=split('INSTALLATION, CONSIDERED','A proper place<br>for every flag.','Site review, product selection, preparation, installation and final checks. Your site, access and foundation requirements shape the plan.','hero','Flagpoles in landscaped grounds beside a building',link('/quote/?need=Flagpole%20Installation','REQUEST INSTALLATION QUOTE','button navy'))
HOME+='<section class="service-band"><div class="wrap"><div>'+section_head('COMMERCIAL FLAG MANAGEMENT','Your flags.<br>Always looking their best.','Build a service plan around your property, your display and your schedule.')+'</div><div class="service-list">'+''.join(f'<a href="{u}"><span>{t}</span><span class="small">{d}</span></a>' for t,u,d in [('Flag replacement','/flag-replacement/','Fresh flags, when needed'),('Rope & hardware','/flagpole-repair/','Resolve wear and damage'),('Scheduled servicing','/flag-service/','A plan for the seasons'),('Multi-location programs','/commercial-accounts/','Coordinate your portfolio')])+'</div>'+button('BUILD A SERVICE PLAN','Commercial%20Flag%20Service')+'</div></section>'
HOME+='<section class="wrap section"><div class="section-title-row">'+section_head('YOUR SETTING. YOUR SOLUTION.','Built around your world.')+link('/industries/','ALL INDUSTRIES','text-link')+'</div>'+cards([('Properties & portfolios','/industries/property-management/','A consistent display across buildings and budgets.'),('Events & festivals','/industries/events/','Flags that make an occasion feel like an occasion.'),('Public & community spaces','/industries/municipalities/','Thoughtful displays for shared places.')])+'</section>'
HOME+='<section class="wrap canada-section"><div>'+section_head('CANADA, CONNECTED','Tell us where.<br>We’ll start there.','Find flags, flagpoles, rentals, installation and service for your property or event.')+link('/locations/','FIND YOUR LOCATION','button navy')+'</div><div class="region-board"><span class="region-label">COAST TO COAST TO COAST</span>'+''.join(link('/locations/'+s+'/',t) for s,t in [('british-columbia','BC'),('alberta','AB'),('saskatchewan','SK'),('manitoba','MB'),('ontario','ON'),('quebec','QC'),('new-brunswick','NB'),('nova-scotia','NS'),('prince-edward-island','PE'),('newfoundland-and-labrador','NL'),('yukon','YT'),('northwest-territories','NT'),('nunavut','NU')])+'</div></section>'
HOME+='<section class="wrap section">'+section_head('STRAIGHTFORWARD FROM THE START','How Waving.ca works.')+steps([('Tell us what you need','A flag, an event, a repair or an entire portfolio.'),('Shape the solution','We review the application, location and requirements.'),('Delivery or installation','Review your quote and arrange delivery or installation.'),('Keep things moving','Add ongoing service when your property needs it.')])+'</section>'
add('/',"Canada’s Flag & Flagpole Company",'Flags, flagpoles, rentals, installation and commercial flag service. Find the right solution for your property, event or organization.',HOME)

def quote_context(path):
 parts=path.strip('/').split('/')
 root=parts[0]
 need=''
 if root=='flags': need='Custom Flags' if len(parts)>1 and parts[1] in ('custom','corporate') else 'Buy Flags'
 elif root=='custom-flags': need='Custom Flags'
 elif root=='flagpoles': need='Buy Flagpole'
 elif root=='flag-rentals': need='Flagpole Rental' if 'temporary-flagpoles' in parts else 'Flag Rental'
 elif root=='flagpole-installation': need='Flagpole Installation'
 elif root in ('flagpole-repair','flagpole-rope-replacement','flagpole-hardware-repair'): need='Flagpole Repair'
 elif root=='flag-replacement': need='Flag Replacement'
 elif root=='commercial-accounts': need='Multi-Location Program'
 elif root in ('flag-service','flagpole-maintenance','flagpole-inspection','half-mast-service'): need='Commercial Flag Service'
 elif root=='services' and len(parts)>1:
  need={'event-setup-takedown':'Flag Rental','seasonal-flag-change':'Flag Replacement','specialist':'Other'}.get(parts[1],'Flagpole Repair')
 elif root=='accessories': need='Other'
 context={}
 if need: context['need']=need
 if need or root in ('locations','industries'): context['topic']=PAGES[path]['title']
 if root=='locations' and len(parts)==3:
  context['city']={'montreal':'Montreal','vancouver':'Vancouver','calgary':'Calgary','ottawa':'Ottawa','toronto':'Toronto'}.get(parts[-1],parts[-1].replace('-',' ').title())
 return '/quote/?'+urlencode(context) if context else '/quote/'

def breadcrumbs(path):
 if path in ('/','/404/'): return '',[]
 routes=['/']
 parts=path.strip('/').split('/')
 for i in range(1,len(parts)):
  parent='/'+('/'.join(parts[:i]))+'/'
  if parent in PAGES: routes.append(parent)
 routes.append(path)
 labels=['Home' if r=='/' else PAGES[r]['title'] for r in routes]
 markup='<nav class="breadcrumbs wrap" aria-label="Breadcrumb"><ol>'+''.join('<li>'+ (link(r,esc(t)) if r!=path else f'<span aria-current="page">{esc(t)}</span>')+'</li>' for r,t in zip(routes,labels))+'</ol></nav>'
 schema=[{'@type':'ListItem','position':i+1,'name':t,'item':CONFIG['origin'].rstrip('/')+r} for i,(r,t) in enumerate(zip(routes,labels))]
 return markup,schema

def search_index():
 groups={'flags':'Flags','custom-flags':'Flags','flagpoles':'Flagpoles','flag-rentals':'Rentals','locations':'Locations','industries':'Industries','resources':'Resources','accessories':'Accessories'}
 for lang,prefix in [('en',''),('fr','/fr')]:
  items=[]
  for path,p in PAGES.items():
   if path in ('/','/search/','/404/','/privacy/','/accessibility/','/quote/','/contact/','/about/'): continue
   category=groups.get(path.strip('/').split('/')[0],'Services')
   translate=tr if lang=='fr' else lambda s:s
   items.append({'url':prefix+path,'title':translate(p['title']),'description':translate(p['description']),'category':category,'categoryLabel':translate(category)})
  (OUT/f'assets/search-{lang}.json').write_text(json.dumps(items,ensure_ascii=False))

def render():
 OUT.mkdir(exist_ok=True)
 (OUT/'assets/config.js').write_text('window.WAVING_CONFIG='+json.dumps({k:CONFIG[k] for k in ['quoteEndpoint','enquiryEmail','phoneE164','phone']})+';')
 origin=CONFIG['origin'].rstrip('/')
 for path,p in PAGES.items():
  url=origin+path
  crumb_html,crumbs=breadcrumbs(path)
  organization={'@type':'Organization','@id':origin+'/#organization','name':CONFIG['brand'],'legalName':CONFIG['legalOperator'],'address':CONFIG['mailingAddress'],'url':origin+'/','telephone':CONFIG['phoneE164'],'email':CONFIG['enquiryEmail'],'logo':{'@type':'ImageObject','url':origin+'/assets/waving-ca-wave-lettering.webp','width':1983,'height':793}}
  website={'@type':'WebSite','@id':origin+'/#website','name':CONFIG['brand'],'url':origin+'/','inLanguage':['en-CA','fr-CA'],'publisher':{'@id':origin+'/#organization'}}
  webpage={'@type':p['kind'],'@id':url+'#webpage','name':p['title'],'description':p['description'],'url':url,'inLanguage':'en-CA','isPartOf':{'@id':origin+'/#website'},'about':{'@id':origin+'/#organization'}}
  if crumbs:webpage['breadcrumb']={'@id':url+'#breadcrumb'}
  schema={'@context':'https://schema.org','@graph':[organization,website,webpage]+([{'@type':'BreadcrumbList','@id':url+'#breadcrumb','itemListElement':crumbs}] if crumbs else [])}
  preview=re.search(r'<img[^>]+src="([^"]+)"[^>]+alt="([^"]*)"',p['body'])
  preview_src,preview_alt=preview.groups() if preview else ('/assets/hero.webp','Flags flying outside a modern commercial building')
  social=f'<meta property="og:site_name" content="Waving.ca"><meta property="og:locale" content="en_CA"><meta property="og:locale:alternate" content="fr_CA"><meta property="og:image" content="{origin}{preview_src}"><meta property="og:image:width" content="1536"><meta property="og:image:height" content="1024"><meta property="og:image:alt" content="{preview_alt}"><meta name="twitter:card" content="summary_large_image">'
  document=f'''<!doctype html><html lang="en-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(p['title'])} | Waving.ca</title><meta name="description" content="{esc(p['description'])}"><meta name="robots" content="{'noindex,follow' if path in NOINDEX_PATHS else 'index,follow,max-image-preview:large'}"><link rel="canonical" href="{esc(url)}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css"><meta name="theme-color" content="#101e2c"><meta property="og:title" content="{esc(p['title'])} | Waving.ca"><meta property="og:description" content="{esc(p['description'])}"><meta property="og:type" content="website"><meta property="og:url" content="{esc(url)}"><script type="application/ld+json">{json.dumps(schema)}</script><script defer src="/assets/site.js"></script></head><body>{header()}<main id="main">{crumb_html}{p['body']}</main>{footer()}</body></html>'''
  document=document.replace('</head>',social+'</head>')
  if path=='/quote/':
   document=re.sub(r'<section class="final-cta wrap">.*?</section>','',document)
   document=document.replace('href="/quote/"','href="#quote-form"')
  else:
   document=document.replace('href="/quote/"',f'href="{esc(quote_context(path))}"')
  document,french=documents(document,path,CONFIG['origin'].rstrip('/'))
  # Resolve contact placeholders after translation, including vanity numbers.
  document,french=(doc.replace('(833) 696-9996',CONFIG['phone']).replace('+18336969996',CONFIG['phoneE164']) for doc in (document,french))
  def version_assets(markup):
   return re.sub(r'(?P<attr>src|href)="(?P<url>/assets/[^"?]+\.(?:css|js))"',lambda m:f'{m["attr"]}="{m["url"]}?v={hashlib.sha256((OUT/m["url"].lstrip("/")).read_bytes()).hexdigest()[:12]}"',markup)
  document,french=version_assets(document),version_assets(french)
  frdest=OUT/'fr'/path.lstrip('/')/'index.html'
  frdest.parent.mkdir(parents=True,exist_ok=True);frdest.write_text(french)
  dest=OUT/path.lstrip('/')/'index.html' if path!='/' else OUT/'index.html'
  dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(document)
 (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+CONFIG['origin']+'/sitemap.xml\n')
 (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+CONFIG['origin']+p+'</loc></url>' for base in ['', '/fr'] for route in PAGES if route not in NOINDEX_PATHS for p in [base+route])+'</urlset>')
 print(f'Built {len(PAGES)} pages in each language')
if __name__=='__main__':
 exec((ROOT/'content.py').read_text(),globals())
 exec((ROOT/'micro_pages.py').read_text(),globals())
 exec((ROOT/'discovery.py').read_text(),globals())
 exec((ROOT/'guides.py').read_text(),globals())
 exec((ROOT/'offerings.py').read_text(),globals())
 exec((ROOT/'media.py').read_text(),globals())
 runtime()
 render()
 search_index()
 shutil.copyfile(OUT/'404/index.html',OUT/'404.html')
