/* Wave local blips and review-only Omni Gemini/Solidify handoffs. No network writes. */
const kinds=new Set(['text','audio-note','code-note','annotation','decision']);
const eventTypes=new Set(['hifi.signal.metrics','wave.blip.created','candidate.draft']);
const idOk=s=>typeof s==='string'&&/^[A-Za-z0-9_-]{1,64}$/.test(s);
const timeOk=s=>typeof s==='string'&&Number.isFinite(Date.parse(s));
function checked(input,prior){
 if(!input||typeof input!=='object'||Array.isArray(input))throw TypeError('Invalid blip');
 const {blipId,kind,text,parentIds,createdAt}=input;
 if(!idOk(blipId))throw Error('Invalid blip ID');
 if(!kinds.has(kind))throw Error('Unsupported blip kind');
 if(typeof text!=='string'||text.length>8000)throw Error('Blip text too long or invalid');
 if(!text.trim())throw Error('Empty blip');
 if(!Array.isArray(parentIds)||parentIds.length>8||new Set(parentIds).size!==parentIds.length)throw Error('Invalid parent list');
 if(!timeOk(createdAt))throw Error('Invalid timestamp');
 if(prior.some(x=>x.blipId===blipId))throw Error('Duplicate blip ID');
 for(const p of parentIds){if(!prior.some(x=>x.blipId===p))throw Error('Unknown parent');}
 return Object.freeze({blipId,kind,text:text.trim(),parentIds:[...parentIds],createdAt,status:'local_draft'});
}
export function appendBlip(previous,input){
 if(!Array.isArray(previous)||previous.length>=256)throw Error('Blip limit exceeded');
 return [...previous,checked(input,previous)];
}
export function validateBlips(value){
 if(!Array.isArray(value)||value.length>256)throw Error('Invalid blip collection');
 return value.reduce((prior,item)=>appendBlip(prior,item),[]);
}
export function draftCandidate(blips,ids){
 if(!Array.isArray(ids)||!ids.length||ids.length>64||new Set(ids).size!==ids.length)throw Error('Invalid source selection');
 const all=validateBlips(blips);
 for(const id of ids){if(!all.some(x=>x.blipId===id))throw Error('Unknown source blip');}
 return {schemaVersion:1,target:'solidify-review-only',status:'draft',approved:false,testsRun:false,sourceBlips:[...ids],requiredChecks:['contracts','audio-quality','rights','human-approval'],source:'local-wave-studio'};
}
export function createEvent({eventId,sessionId,type,createdAt,payload}){
 if(!idOk(eventId)||!idOk(sessionId)||!eventTypes.has(type)||!timeOk(createdAt))throw Error('Unsupported or invalid event');
 if(!payload||typeof payload!=='object'||Array.isArray(payload))throw Error('Invalid payload');
 if(JSON.stringify(payload).length>2048)throw Error('Payload limit exceeded');
 return {schemaVersion:1,eventId,sessionId,type,createdAt,visibility:'local',payload:structuredClone(payload)};
}
