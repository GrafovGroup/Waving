from pathlib import Path
p=Path('build.py');s=p.read_text()
s=s.replace("{''.join(link(u,t) for t,u in NAV)}</nav>","{navigation()}</nav>")
s=s.replace("def footer():",'''def navigation():
 groups={
 'FLAGS':[(x[1],'/flags/'+x[0]+'/') for x in FLAGS],
 'FLAGPOLES':[(x[1],'/flagpoles/'+x[0]+'/') for x in POLES],
 'SERVICES':[(x[1],'/'+x[0]+'/') for x in SERVICES]+[('Commercial flag management','/flag-service/'),('Multi-location accounts','/commercial-accounts/')],
 'RENTALS':[(x[1],'/flag-rentals/'+x[0]+'/') for x in RENTALS]
 }
 result=''
 for title,url in NAV:
  if title in groups:
   result+=f'<details class="nav-group"><summary>{title}</summary><div class="mega"><a class="mega-overview" href="{url}">EXPLORE ALL {title}</a><div>'+''.join(link(u,t.upper()) for t,u in groups[title])+'</div></div></details>'
  else: result+=link(url,title)
 return result

def footer():''')
s=s.replace("document=f'''<!doctype", "document=f'''<!doctype")
s=s.replace("dest=OUT/path.lstrip", "document=document.replace('(833) 696-9996',CONFIG['phone']).replace('+18336969996',CONFIG['phoneE164'])\n  dest=OUT/path.lstrip")
s=s.replace("['quoteEndpoint','enquiryEmail','phoneE164']", "['quoteEndpoint','enquiryEmail','phoneE164','phone']")
p.write_text(s)
p=Path('dist/assets/quote.js');s=p.read_text();s=s.replace("if(!el.checkValidity())", "if((el.required&&typeof el.value==='string'&&!el.value.trim())||!el.checkValidity())")
s=s.replace("['Preferred contact',data.preferred]]", "['Preferred contact',data.preferred],...Object.entries(data).filter(([k,v])=>v&&!['need','city','province','postal','name','email','phone','preferred','notes','consent','rentalStart','rentalEnd'].includes(k)).map(([k,v])=>[({flagType:'Flag type',quantity:'Quantity',dimensions:'Dimensions',poles:'Flagpoles',height:'Pole height',existingPole:'Existing pole',rentalPoles:'Poles required',eventDate:'Event date',setting:'Setting',installation:'Installation',delivery:'Delivery',requiredDate:'Preferred date',frequency:'Service plan',locations:'Locations',issue:'Repair issue',address:'Street address',company:'Company',artwork:'Artwork',otherNeed:'Other requirements'})[k]||k,v])]")
p.write_text(s)
