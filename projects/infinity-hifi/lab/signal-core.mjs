/* Infinity HI-FI / Wave Tech: local PCM measurements and reversible presets. */
export const profiles=Object.freeze({
 original:Object.freeze({dry:1,wet:0,highpass:20,eqHz:1800,eqDb:0,threshold:-24,ratio:1,outputGain:1}),
 speech:Object.freeze({dry:0,wet:1,highpass:95,eqHz:2600,eqDb:2.5,threshold:-24,ratio:2.1,outputGain:0.85}),
 phone:Object.freeze({dry:0,wet:1,highpass:140,eqHz:2400,eqDb:2,threshold:-27,ratio:2.5,outputGain:0.8}),
 night:Object.freeze({dry:0,wet:1,highpass:65,eqHz:1800,eqDb:0,threshold:-30,ratio:3,outputGain:0.65})
});
export function resolveProfile(name){
 if(!Object.hasOwn(profiles,name))throw Error('Unknown audio profile');
 return profiles[name];
}
export function measureSamples(samples){
 if(!(samples instanceof Float32Array))throw TypeError('Expected Float32Array');
 if(!samples.length)throw RangeError('Expected nonempty sample buffer');
 let sum=0,peak=0;
 for(const v of samples){
  if(!Number.isFinite(v))throw Error('Non-finite signal sample');
  const a=Math.abs(v);sum+=v*v;if(a>peak)peak=a;
 }
 const rms=Math.sqrt(sum/samples.length);
 return {samples:samples.length,rms,peak,rmsDbfs:rms?20*Math.log10(rms):null,peakDbfs:peak?20*Math.log10(peak):null,clipped:peak>=0.999};
}
