from pathlib import Path
import json, html, re, shutil
from bilingual import documents, runtime
ROOT=Path(__file__).parent
OUT=ROOT/'dist'
CONFIG=json.loads((ROOT/'site-config.json').read_text())
PAGES={}
def esc(s): return html.escape(str(s),quote=True)
def link(url,label,cls=''): return f'<a class="{cls}" href="{url}">{label}</a>'
def button(label='GET A QUOTE',need=''): return link('/quote/'+('?need='+need if need else ''),label,'button')
def img(kind='hero',alt='',cls=''): return f'<img class="{cls}" src="/assets/{kind}.webp" alt="{esc(alt)}" width="1536" height="1024" loading="lazy" decoding="async">'
NAV=[('FLAGS','/flags/'),('FLAGPOLES','/flagpoles/'),('RENTALS','/flag-rentals/'),('INSTALLATION','/flagpole-installation/'),('SERVICES','/services/'),('INDUSTRIES','/industries/'),('LOCATIONS','/locations/'),('RESOURCES','/resources/'),('ABOUT','/about/'),('CONTACT','/contact/')]
LOGO='<span class="brand-logo"><img src="/assets/waving-logo.png" alt="" width="1774" height="887" decoding="async"></span>'
def header():
 return f'''<a class="skip" href="#main">Skip to content</a><div class="utility"><span>FLAGS. FLAGPOLES. INSTALLATION. SERVICE.</span><a href="tel:+18336969996">(833) 696-9996</a></div><header class="site-header"><div class="header-main"><a class="brand-link" href="/" aria-label="Waving home">{LOGO}</a><div class="header-right"><span class="header-note">Made for places.<br>Ready for possibilities.</span>{button()}<button class="menu-toggle" aria-expanded="false" aria-controls="navigation">MENU</button></div></div><nav id="navigation" aria-label="Main navigation">{navigation()}</nav></header>'''
def navigation():
 groups={
 'FLAGS':[(x[1],'/flags/'+x[0]+'/') for x in FLAGS]+[('Parts & accessories','/accessories/')],
 'FLAGPOLES':[(x[1],'/flagpoles/'+x[0]+'/') for x in POLES],
 'SERVICES':[(x[1],'/'+x[0]+'/') for x in SERVICES]+[('Commercial flag management','/flag-service/'),('Multi-location accounts','/commercial-accounts/'),('Specialist services','/services/specialist/'),('Parts & accessories','/accessories/')],
 'RENTALS':[(x[1],'/flag-rentals/'+x[0]+'/') for x in RENTALS]
 }
 result=''
 for title,url in NAV:
  if title in groups:
   result+=f'<details class="nav-group"><summary>{title}</summary><div class="mega"><a class="mega-overview" href="{url}">EXPLORE ALL {title}</a><div>'+''.join(link(u,t.upper()) for t,u in groups[title])+'</div></div></details>'
  else: result+=link(url,title)
 return result

def footer():
 return f'''<section class="final-cta wrap"><div><p class="eyebrow">LET’S GET STARTED</p><h2>Ready to get waving?</h2><p>Tell us what you need and where you need it.</p></div>{button()}</section><footer><div class="wrap footer-grid"><div><a class="brand-link" href="/" aria-label="Waving home">{LOGO}</a><p>Flags for a place.<br>Service for the long run.</p><a class="phone" href="tel:+18336969996">(833) 696-9996</a><p><a href="mailto:{esc(CONFIG['enquiryEmail'])}">{esc(CONFIG['enquiryEmail'])}</a></p></div><div><h3>EXPLORE</h3>{''.join(link(u,t) for t,u in NAV[:5])}</div><div><h3>WAVING</h3>{''.join(link(u,t) for t,u in NAV[5:])}</div><div><h3>LET’S TALK</h3><p>One flag or a whole portfolio.<br>Start with what you have in mind.</p>{button('REQUEST A QUOTE')}<p class="small">On-site service depends on location, access and project requirements.</p></div></div><div class="wrap footer-bottom"><span>© {2026} Waving. Keep Canada waving.</span><div><a href="/privacy/">PRIVACY</a><a href="/accessibility/">ACCESSIBILITY</a></div></div></footer><div class="mobile-actions"><a href="tel:+18336969996">CALL</a><a href="/quote/">GET A QUOTE</a></div>'''
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
HOME='''<section class="home-hero"><div class="hero-photo"><img src="/assets/hero.webp" alt="Canadian and neutral flags flying beside a contemporary commercial property" width="1536" height="1024" fetchpriority="high"></div><div class="hero-content wrap"><p class="eyebrow">FOR THE PLACES THAT BRING US TOGETHER</p><h1>CANADA’S<br>FLAG &amp;<br>FLAGPOLE<br>COMPANY<span>.</span></h1><p>Flags, flagpoles, rentals, installation and ongoing service for businesses, events, institutions and properties across Canada.</p><div class="actions"><a class="button" href="/quote/">GET A QUOTE</a><a class="button outline light" href="/flags/">SHOP FLAGS</a></div><div class="hero-caption"><span>FROM ONE FLAG</span><span>TO EVERY LOCATION.</span></div></div></section>'''
HOME+='<section class="quick-wrap wrap"><p class="eyebrow">WHAT DO YOU NEED?</p><div class="quick-links">'+''.join(link(u,t) for t,u in [('BUY FLAGS','/flags/'),('CUSTOM FLAGS','/custom-flags/'),('RENT FLAGS','/flag-rentals/'),('FLAGPOLE INSTALLATION','/flagpole-installation/'),('FLAGPOLE REPAIR','/flagpole-repair/'),('COMMERCIAL FLAG SERVICE','/flag-service/')])+'</div></section>'
HOME+='<section class="wrap section"><div class="section-title-row">'+section_head('SOMETHING WORTH FLYING','For every place.<br>For every purpose.')+link('/flags/','EXPLORE ALL FLAGS','text-link')+'</div><div class="feature-grid"><a class="feature-tile" href="/flags/canada/">'+img('hero','Canadian flag flying from an aluminum flagpole')+'<div><p class="eyebrow">A FAMILIAR SYMBOL. A FRESH START.</p><h3>Canadian flags</h3></div></a><a class="feature-tile" href="/custom-flags/">'+img('event','Navy and white flags at an outdoor event')+'<div><p class="eyebrow">MAKE YOUR MARK</p><h3>Your brand. In motion.</h3></div></a></div><div class="category-links">'+''.join(link('/flags/'+s+'/',t) for s,t in [('provincial','PROVINCIAL & TERRITORIAL'),('international','INTERNATIONAL'),('corporate','CORPORATE'),('municipal','MUNICIPAL'),('indigenous','INDIGENOUS'),('event','EVENT'),('sports','SPORTS'),('feather','FEATHER'),('banner','BANNER')])+'</div></section>'
HOME+=split('A STRONG FOUNDATION','The right pole.<br>The right presence.','From a residential entrance to a multi-pole commercial display, start with a flagpole suited to the setting, flag size and exposure. We help bring the pieces together.','hardware','Aluminum flagpole with cleat and secured halyard',link('/flagpoles/','EXPLORE FLAGPOLES','button navy'))
HOME+='<section class="rental-band"><div class="rental-image">'+img('event','Portable event flags arranged across an outdoor plaza')+'</div><div class="rental-copy"><p class="eyebrow">BIG OCCASION. SHORT-TERM SOLUTION.</p><h2>Need flags<br>temporarily?</h2><p>Set the scene for a conference, ceremony, festival or film production. Explore flags, portable poles and coordinated event installation.</p><div class="pill-row"><span>EVENTS</span><span>FESTIVALS</span><span>CEREMONIES</span><span>FILM</span></div>'+button('GET RENTAL PRICING','Flag%20Rental')+'</div></section>'
HOME+=split('INSTALLATION, CONSIDERED','A proper place<br>for every flag.','Site review, product selection, preparation, installation and final checks. Your site, access and foundation requirements shape the plan.','hero','Flagpoles in landscaped grounds beside a building',link('/flagpole-installation/','REQUEST INSTALLATION QUOTE','button navy'))
HOME+='<section class="service-band"><div class="wrap"><div>'+section_head('COMMERCIAL FLAG MANAGEMENT','Your flags.<br>Always looking their best.','Build a service plan around your property, your display and your schedule.')+'</div><div class="service-list">'+''.join(f'<a href="{u}"><span>{t}</span><span class="small">{d}</span></a>' for t,u,d in [('Flag replacement','/flag-replacement/','Fresh flags, when needed'),('Rope & hardware','/flagpole-repair/','Resolve wear and damage'),('Scheduled servicing','/flag-service/','A plan for the seasons'),('Multi-location programs','/commercial-accounts/','Coordinate your portfolio')])+'</div>'+button('BUILD A SERVICE PLAN','Commercial%20Flag%20Service')+'</div></section>'
HOME+='<section class="wrap section"><div class="section-title-row">'+section_head('YOUR SETTING. YOUR SOLUTION.','Built around your world.')+link('/industries/','ALL INDUSTRIES','text-link')+'</div>'+cards([('Properties & portfolios','/industries/property-management/','A consistent display across buildings and budgets.'),('Events & festivals','/industries/events/','Flags that make an occasion feel like an occasion.'),('Public & community spaces','/industries/municipalities/','Thoughtful displays for shared places.')])+'</section>'
HOME+='<section class="wrap canada-section"><div>'+section_head('CANADA, CONNECTED','Tell us where.<br>We’ll start there.','Explore regional planning information and request product delivery, rentals or on-site service. Availability is confirmed for your location and scope.')+link('/locations/','FIND YOUR LOCATION','button navy')+'</div><div class="region-board"><span class="region-label">COAST TO COAST TO COAST</span>'+''.join(link('/locations/'+s+'/',t) for s,t in [('british-columbia','BC'),('alberta','AB'),('saskatchewan','SK'),('manitoba','MB'),('ontario','ON'),('quebec','QC'),('new-brunswick','NB'),('nova-scotia','NS'),('prince-edward-island','PE'),('newfoundland-and-labrador','NL'),('yukon','YT'),('northwest-territories','NT'),('nunavut','NU')])+'</div></section>'
HOME+='<section class="wrap section">'+section_head('STRAIGHTFORWARD FROM THE START','How Waving works.')+steps([('Tell us what you need','A flag, an event, a repair or an entire portfolio.'),('Shape the solution','We review the application, location and requirements.'),('Delivery or installation','Scope, availability and arrangements are confirmed in your quote.'),('Keep things moving','Add ongoing service when your property needs it.')])+'</section>'
add('/',"Canada’s Flag & Flagpole Company",'Flags, flagpoles, rentals, installation and commercial flag service. Find the right solution for your property, event or organization.',HOME)

def render():
 OUT.mkdir(exist_ok=True)
 for path,p in PAGES.items():
  url=CONFIG['origin'].rstrip('/')+path
  crumbs=[]
  if path!='/':
   crumbs=[{'@type':'ListItem','position':1,'name':'Home','item':CONFIG['origin']+'/'},{'@type':'ListItem','position':2,'name':p['title'],'item':url}]
  schema={'@context':'https://schema.org','@graph':[{'@type':'Organization','@id':CONFIG['origin']+'/#organization','name':'Waving','url':CONFIG['origin'],'telephone':CONFIG['phoneE164']},{'@type':p['kind'],'name':p['title'],'description':p['description'],'url':url}]+([{'@type':'BreadcrumbList','itemListElement':crumbs}] if crumbs else [])}
  document=f'''<!doctype html><html lang="en-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(p['title'])} | Waving</title><meta name="description" content="{esc(p['description'])}"><meta name="robots" content="{'noindex,follow' if path=='/404/' else 'index,follow'}"><link rel="canonical" href="{esc(url)}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css"><meta name="theme-color" content="#101e2c"><meta property="og:title" content="{esc(p['title'])} | Waving"><meta property="og:description" content="{esc(p['description'])}"><meta property="og:type" content="website"><meta property="og:url" content="{esc(url)}"><script type="application/ld+json">{json.dumps(schema)}</script><script defer src="/assets/site.js"></script></head><body>{header()}<main id="main">{p['body']}</main>{footer()}</body></html>'''
  document=document.replace('(833) 696-9996',CONFIG['phone']).replace('+18336969996',CONFIG['phoneE164'])
  document,french=documents(document,path,CONFIG['origin'].rstrip('/'))
  frdest=OUT/'fr'/path.lstrip('/')/'index.html'
  frdest.parent.mkdir(parents=True,exist_ok=True);frdest.write_text(french)
  dest=OUT/path.lstrip('/')/'index.html' if path!='/' else OUT/'index.html'
  dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(document)
 (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+CONFIG['origin']+'/sitemap.xml\n')
 (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+CONFIG['origin']+p+'</loc></url>' for base in ['', '/fr'] for route in PAGES if route!='/404/' for p in [base+route])+'</urlset>')
 (OUT/'assets/config.js').write_text('window.WAVING_CONFIG='+json.dumps({k:CONFIG[k] for k in ['quoteEndpoint','enquiryEmail','phoneE164','phone']})+';')
 print(f'Built {len(PAGES)} pages in each language')
if __name__=='__main__':
 exec((ROOT/'content.py').read_text(),globals())
 exec((ROOT/'micro_pages.py').read_text(),globals())
 render()
 runtime()
 shutil.copyfile(OUT/'404/index.html',OUT/'404.html')
