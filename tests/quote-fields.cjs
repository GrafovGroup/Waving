const assert=require('node:assert/strict');
const fields=require('../dist/assets/quote-fields.js');
const needs=['Buy Flags','Custom Flags','Buy Flagpole','Flagpole Installation','Flag Rental','Flagpole Rental','Flagpole Repair','Flag Replacement','Commercial Flag Service','Multi-Location Program','Other'];
const values={need:'Flag Rental',name:'Synthetic QA',email:'qa@example.invalid',city:'Test city',consent:true,notes:'Keep this note',topic:'Test guide',flagQuantity:'4',poleQuantity:'2',rentalQuantity:'6',flagSize:'0.9 x 1.8 m',deliveryDate:'2027-05-01',completionDate:'2027-08-01',artworkStatus:'Artwork ready',poleHeight:'6 m',setting:'Outdoors',installation:'Supply only',installationType:'New display',rentalStart:'2027-06-10',rentalEnd:'2027-06-12',rentalPackage:'Flag only',repairIssue:'Pole damage',siteCount:'5',serviceFrequency:'Seasonal',unexpected:'do not send'};
for(const need of needs){
 const state={...values,need};const before=JSON.stringify(state);const payload=fields.filterData(state);const allowed=new Set(['need','name','email','city','consent','notes','topic',...(fields.groupForNeed(need)?.fields||[]).map(f=>f[0])]);
 assert.deepEqual(new Set(Object.keys(payload)),allowed,need);
 assert.equal(JSON.stringify(state),before,'Changing need must not erase previous inputs');
 assert.equal(payload.notes,'Keep this note');
}
assert.equal(fields.groupForNeed('unknown'),null);
assert.ok(fields.dateError({...values,rentalEnd:'2027-06-09'}));
assert.equal(fields.dateError({...values,rentalEnd:'2027-06-10'}),'');
assert.equal(fields.dateError({...values,rentalEnd:''}),'');
assert.equal(fields.dateError({...values,need:'Buy Flags',rentalEnd:'2027-06-09'}),'');
assert.ok(!('consent' in fields.filterData({need:'Other',consent:false,notes:''})));
for(const [id,label] of [['flag-only','Flag only'],['display-system','Flag, pole and base'],['event-service','Display with delivery and setup']]){
 const preset=fields.prefill(new URLSearchParams({need:'Flag Rental',package:id}));
 assert.equal(preset.rentalPackage,label);
 assert.equal(fields.filterData({need:'Flag Rental',...preset}).rentalPackage,label);
 assert.ok(!('rentalPackage' in fields.filterData({need:'Buy Flags',...preset})));
}
assert.deepEqual(fields.prefill(new URLSearchParams({need:'Buy Flags',package:'flag-only'})),{});
assert.deepEqual(fields.prefill(new URLSearchParams({need:'Flag Rental',package:'unknown'})),{});
console.log('PASS: all 11 request types, only relevant fields submitted, previous entries preserved, optional and reversed rental dates, unknown input excluded.');
