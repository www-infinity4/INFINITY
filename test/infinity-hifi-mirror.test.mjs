import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const read=path=>readFileSync(new URL('../'+path,import.meta.url),'utf8');
test('INFINITY existing blueprint links both working source pages',()=>{
 const root=read('projects/infinity-hifi/index.html'),studio=read('projects/infinity-hifi/lab/index.html'),desk=read('projects/infinity-hifi/lab/research.html');
 assert.match(root,/href="lab\/"/);
 assert.match(root,/href="lab\/research.html"/);
 assert.match(studio,/href="\.\/research.html"/);
 assert.match(desk,/Research and source files/);
 assert.match(root,/The full architecture is still a blueprint/);
});
test('mirror references local source, not external backend or private records',()=>{
 const dir='projects/infinity-hifi/lab/';
 const studio=read(dir+'studio.mjs');
 const desk=read(dir+'research.html');
 for(const path of ['signal-core.mjs','wave-core.mjs','studio.css','index.html'])assert.doesNotThrow(()=>read(dir+path));
 assert.match(studio,/createObjectURL\(chosen\)/);
 assert.doesNotMatch(studio,/\b(?:fetch|XMLHttpRequest|WebSocket|sendBeacon|getUserMedia)\s*\(/);
 assert.match(desk,/github.com\/www-infinity4\/Infinity-HiFi\/blob/);
 assert.match(desk,/ncbi\.nlm\.nih\.gov/);
});
