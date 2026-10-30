const {JSDOM,VirtualConsole}=require('jsdom');
const fs=require('fs'),assert=require('node:assert/strict');
for (const path of ['demo/index.html','.local/private/工具/求职进度面板/dashboard.html']) {
 const errors=[]; const console=new VirtualConsole();console.on('jsdomError',e=>errors.push(e.message));
 const dom=new JSDOM(fs.readFileSync(path,'utf8'),{url:'https://compass.invalid/',runScripts:'dangerously',virtualConsole:console,beforeParse(w){w.matchMedia=()=>({matches:false,addEventListener(){},removeEventListener(){}});w.HTMLElement.prototype.scrollIntoView=function(){};}});
 const d=dom.window.document;
 assert.equal(d.querySelectorAll('#tabs [role=tab]').length,4);
 for(const name of ['today','discovered','todo','progress']) {
  d.querySelector(`[data-tab="${name}"]`).click();
  assert.equal(d.querySelector(`[data-tab="${name}"]`).getAttribute('aria-selected'),'true');
 }
 assert.equal(errors.length,0,errors.join('\n'));
 dom.window.close();
}
console.log('Customized demo and empty private workspace navigation passed.');
