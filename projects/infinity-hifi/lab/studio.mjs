import {measureSamples,resolveProfile} from './signal-core.mjs';
import {appendBlip,validateBlips,draftCandidate,createEvent} from './wave-core.mjs';
const $=id=>document.getElementById(id);
const player=$('player'),file=$('audioFile'),mode=$('profile'),audioStatus=$('audioStatus');
const canvas=$('waveCanvas'),ctx2d=canvas.getContext('2d');
const scale=x=>x===null?'silence':x.toFixed(1);
const id=()=>crypto.randomUUID().replaceAll('-','_');
const status=(node,message)=>{node.textContent=message;};
let audioCtx=null,analyser=null,graph=null,audioObjectUrl=null,frame=null,blips=[];
function drawZero(){
 ctx2d.clearRect(0,0,canvas.width,canvas.height);
 ctx2d.strokeStyle='#6b899d';ctx2d.beginPath();ctx2d.moveTo(0,75);ctx2d.lineTo(canvas.width,75);ctx2d.stroke();
}
drawZero();
function updateProfile(){
 if(!graph)return;
 const p=resolveProfile(mode.value);
 graph.dry.gain.value=p.dry;graph.wet.gain.value=p.wet*p.outputGain;
 graph.highpass.frequency.value=p.highpass;graph.eq.frequency.value=p.eqHz;
 graph.eq.gain.value=p.eqDb;graph.compressor.threshold.value=p.threshold;graph.compressor.ratio.value=p.ratio;
 status(audioStatus,mode.value==='original'?'Playing the original dry signal without EQ or compression.':'Active local profile: '+mode.selectedOptions[0].textContent+'.');
}
async function enableAudio(){
 if(!player.src)return;
 if(!audioCtx){
  const AudioContextClass=window.AudioContext||window.webkitAudioContext;
  if(!AudioContextClass){status(audioStatus,'This browser does not support Web Audio processing. Original file playback remains available.');return;}
  audioCtx=new AudioContextClass();
  const source=audioCtx.createMediaElementSource(player);
  const dry=audioCtx.createGain(),wet=audioCtx.createGain();
  const highpass=audioCtx.createBiquadFilter();highpass.type='highpass';
  const eq=audioCtx.createBiquadFilter();eq.type='peaking';eq.Q.value=0.85;
  const compressor=audioCtx.createDynamicsCompressor();compressor.attack.value=0.005;compressor.release.value=0.2;
  analyser=audioCtx.createAnalyser();analyser.fftSize=2048;analyser.smoothingTimeConstant=0.65;
  source.connect(dry);dry.connect(analyser);
  source.connect(highpass);highpass.connect(eq);eq.connect(compressor);compressor.connect(wet);wet.connect(analyser);
  analyser.connect(audioCtx.destination);
  graph={dry,wet,highpass,eq,compressor};
  updateProfile();
 }
 await audioCtx.resume();
}
function renderSamples(){
 if(!analyser||player.paused)return;
 const pcm=new Float32Array(analyser.fftSize);analyser.getFloatTimeDomainData(pcm);
 const measure=measureSamples(pcm);
 $('rms').textContent=scale(measure.rmsDbfs);$('peak').textContent=scale(measure.peakDbfs);
 $('clip').textContent=measure.clipped?'YES':'No';
 const bins=new Float32Array(analyser.frequencyBinCount);analyser.getFloatFrequencyData(bins);
 let max=-Infinity,idx=-1;
 for(let i=1;i<bins.length;i++)if(bins[i]>max){max=bins[i];idx=i;}
 $('frequency').textContent=max>-100&&idx>=0?Math.round(idx*audioCtx.sampleRate/analyser.fftSize).toString():'—';
 const w=canvas.width,h=canvas.height;ctx2d.clearRect(0,0,w,h);ctx2d.lineWidth=2;ctx2d.strokeStyle='#7be1e5';ctx2d.beginPath();
 for(let i=0;i<pcm.length;i+=2){const x=i/(pcm.length-1)*w,y=h*(.5-.44*pcm[i]);if(i===0)ctx2d.moveTo(x,y);else ctx2d.lineTo(x,y)}ctx2d.stroke();
 frame=requestAnimationFrame(renderSamples);
}
file.addEventListener('change',()=>{
 player.pause();if(audioObjectUrl)URL.revokeObjectURL(audioObjectUrl);
 const chosen=file.files?.[0];audioObjectUrl=null;player.removeAttribute('src');player.load();
 if(!chosen){status(audioStatus,'No audio selected.');return;}
 if(chosen.type&&!chosen.type.startsWith('audio/')){status(audioStatus,'Choose an audio file supported by your browser.');return;}
 audioObjectUrl=URL.createObjectURL(chosen);player.src=audioObjectUrl;
 status(audioStatus,'Local file selected. Press Play. No audio has been uploaded.');
});
mode.addEventListener('change',updateProfile);
player.addEventListener('play',async()=>{try{await enableAudio();cancelAnimationFrame(frame);renderSamples()}catch{status(audioStatus,'Enhanced audio unavailable. Pause or choose another file.')}});
player.addEventListener('pause',()=>cancelAnimationFrame(frame));
player.addEventListener('ended',()=>cancelAnimationFrame(frame));
window.addEventListener('pagehide',()=>{if(audioObjectUrl)URL.revokeObjectURL(audioObjectUrl);});
function renderBlips(){
 const target=$('blips'),parent=$('parent');target.replaceChildren();parent.replaceChildren();
 parent.appendChild(new Option('New root branch',''));
 if(!blips.length){const p=document.createElement('p');p.textContent='No blips yet.';target.appendChild(p);return;}
 for(const b of blips){
  parent.appendChild(new Option(b.blipId+' · '+b.text.slice(0,35),b.blipId));
  const article=document.createElement('article');article.className='blip';
  const name=document.createElement('strong');name.textContent=b.kind+' · '+b.blipId;
  const meta=document.createElement('div');meta.className='meta';meta.textContent=b.createdAt+(b.parentIds.length?' · reply to '+b.parentIds.join(', '):' · root');
  const body=document.createElement('p');body.textContent=b.text;
  article.append(name,meta,body);target.appendChild(article);
 }
}
$('addBlip').addEventListener('click',()=>{
 try{
  const parent=$('parent').value;
  const raw=$('blipText').value.trim();if(!raw)throw Error('Write a note before adding a blip');
  const position=player.src&&Number.isFinite(player.currentTime)?' [media '+player.currentTime.toFixed(1)+'s]':'';
  const next=appendBlip(blips,{blipId:'blip_'+id(),kind:$('blipType').value,text:raw+position,parentIds:parent?[parent]:[],createdAt:new Date().toISOString()});
  blips=next;renderBlips();$('blipText').value='';
  status($('waveStatus'),'Saved in this tab only. '+blips.length+' blip(s). Export to keep them.');
 }catch(e){status($('waveStatus'),e.message||'Blip rejected.');}
});
function download(name,object){
 const data=new Blob([JSON.stringify(object,null,2)],{type:'application/json'});
 const url=URL.createObjectURL(data);const anchor=document.createElement('a');anchor.href=url;anchor.download=name;anchor.click();
 setTimeout(()=>URL.revokeObjectURL(url),60000);
}
$('exportBlips').addEventListener('click',()=>{
 download('infinity-wave-local.json',{schemaVersion:1,visibility:'local',blips});
 status($('waveStatus'),'Your Wave JSON was prepared for local download. No server upload.');
});
$('exportCandidate').addEventListener('click',()=>{
 try{
  const candidate=draftCandidate(blips,blips.map(x=>x.blipId));
  const event=createEvent({eventId:'evt_'+id(),sessionId:'local_hifi',type:'candidate.draft',createdAt:new Date().toISOString(),payload:{sourceCount:candidate.sourceBlips.length,status:'draft'}});
  download('solidify-review-draft.json',{candidate,event,blips});
  status($('waveStatus'),'Review-only Solidify draft prepared. No tests, approval, GitHub webhook or publishing occurred.');
 }catch(e){status($('waveStatus'),e.message||'Cannot prepare candidate.');}
});
$('importBlips').addEventListener('change',async event=>{
 const selected=event.target.files?.[0];if(!selected)return;
 try{
  if(selected.size>2_000_000)throw Error('Import exceeds 2 MB cap');
  const json=JSON.parse(await selected.text());
  if(json.schemaVersion!==1||json.visibility!=='local')throw Error('Unsupported Wave JSON version/visibility');
  const incoming=validateBlips(json.blips);blips=incoming;renderBlips();
  status($('waveStatus'),'Imported '+incoming.length+' local blips. Nothing uploaded, approved or published.');
 }catch(e){status($('waveStatus'),'Import rejected: '+(e.message||'invalid file'));}
 finally{event.target.value='';}
});
renderBlips();
