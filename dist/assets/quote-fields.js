(function(root){'use strict';
const groups={
 flags:{title:'Flag details',fields:[['flagQuantity','Quantity','number'],['flagSize','Flag size, if known','text'],['deliveryDate','Preferred delivery date','date']]},
 custom:{title:'Custom flag details',fields:[['flagQuantity','Quantity','number'],['flagSize','Flag size, if known','text'],['deliveryDate','Preferred delivery date','date'],['artworkStatus','Artwork status','select',['Artwork ready','Artwork in progress','I need help with artwork']]]},
 poles:{title:'Flagpole details',fields:[['poleQuantity','Number of poles','number'],['poleHeight','Approximate pole height','text'],['setting','Display setting','select',['Outdoors','Indoors','Not sure yet']],['installation','Installation requirements','select',['Supply only','Installation requested','Not sure yet']]]},
 installation:{title:'Installation details',fields:[['poleQuantity','Number of poles','number'],['poleHeight','Approximate pole height','text'],['installationType','Installation type','select',['New display','Replace an existing pole','Not sure yet']],['completionDate','Preferred completion date','date']]},
 rental:{title:'Rental details',fields:[['rentalStart','Equipment needed from','date'],['rentalEnd','Equipment available for collection','date'],['rentalQuantity','Number of flags or displays','number'],['rentalPackage','Rental package','select',['Flag only','Flag, pole and base','Display with delivery and setup','Not sure yet']]]},
 repair:{title:'Repair details',fields:[['repairIssue','What needs attention?','select',['Rope or hardware','Flag stuck or not moving','Pole damage','Other or not sure']],['poleHeight','Approximate pole height','text'],['poleQuantity','Number of poles','number']]},
 service:{title:'Service details',fields:[['siteCount','Number of locations','number'],['poleQuantity','Total number of poles','number'],['serviceFrequency','Service frequency','select',['One-time request','Seasonal','Quarterly','Let’s discuss a schedule']]]}
};
const mapping={'Buy Flags':'flags','Flag Replacement':'flags','Custom Flags':'custom','Buy Flagpole':'poles','Flagpole Installation':'installation','Flag Rental':'rental','Flagpole Rental':'rental','Flagpole Repair':'repair','Commercial Flag Service':'service','Multi-Location Program':'service'};
const base=['need','name','email','phone','city','notes','consent','topic'];
const packages={'flag-only':'Flag only','display-system':'Flag, pole and base','event-service':'Display with delivery and setup'};
function prefill(params){return ['Flag Rental','Flagpole Rental'].includes(params.get('need'))&&Object.hasOwn(packages,params.get('package'))?{rentalPackage:packages[params.get('package')]}:{}}
function groupForNeed(need){return groups[mapping[need]]||null}
function filterData(data){const allowed=new Set([...base,...(groupForNeed(data.need)?.fields||[]).map(f=>f[0])]);return Object.fromEntries(Object.entries(data).filter(([k,v])=>allowed.has(k)&&v!==''&&v!==false))}
function dateError(data){return mapping[data.need]==='rental'&&data.rentalStart&&data.rentalEnd&&data.rentalEnd<data.rentalStart?'Collection cannot be before the equipment is needed.':''}
const api={groups,groupForNeed,filterData,dateError,prefill};
if(typeof module==='object'&&module.exports)module.exports=api;
else root.WAVING_QUOTE_FIELDS=api;
})(typeof window==='undefined'?{}:window);
