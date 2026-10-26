const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('dist/assets/quote.js','utf8');
const submit = source.slice(source.indexOf('async function submit()'), source.lastIndexOf('render();})();'));
async function run(response) {
  const success = {hidden:true,setAttribute(){},focus(){}};
  const context = {window:{WAVING_CONFIG:{quoteEndpoint:'https://example.invalid/test'}},
    form:{hidden:false,elements:{_gotcha:{value:''}},setAttribute(){},removeAttribute(){}},
    document:{documentElement:{lang:'en-CA'},querySelector:()=>success},
    data:{need:'Buy Flags',name:'Synthetic QA'},files:[],started:Date.now()-10000,
    busy:false,next:{},prev:{},FormData,AbortController,setTimeout,clearTimeout,
    tr:s=>s,event(){},showError(message){context.error=message},
    fetch:async()=>{if(response instanceof Error)throw response;return response}};
  vm.createContext(context); await vm.runInContext(submit+';submit()',context);
  return {context,success};
}
(async()=>{
  for(const response of [
    {ok:true,json:async()=>({})},
    {ok:true,json:async()=>{throw new Error('HTML response')}},
    {ok:false,json:async()=>({ok:true})},
    {ok:true,json:async()=>({ok:false})},
    {ok:true,json:async()=>({ok:true,errors:[{message:'rejected'}]})},
    new Error('network unavailable')
  ]) {const {context,success}=await run(response);assert.equal(context.form.hidden,false);assert.equal(success.hidden,true);assert.ok(context.error);assert.equal(context.busy,false);assert.equal(context.data.name,'Synthetic QA');}
  const {context,success}=await run({ok:true,json:async()=>({ok:true})});assert.equal(context.form.hidden,true);assert.equal(success.hidden,false);assert.equal(context.next.disabled,false);
  console.log('PASS: confirmed acceptance; malformed JSON, ambiguous success, HTTP errors, provider rejection and network errors preserve entries. No network requests sent.');
})().catch(e=>{console.error(e);process.exit(1)});
