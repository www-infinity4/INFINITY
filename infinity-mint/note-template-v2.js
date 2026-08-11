/* Infinity Mint approved note renderer.
 * Canonical identity remains the full Commit Token hash. The face serial is a readable projection.
 * The approved master artwork should be installed at assets/infinity-capital-note-master.webp.
 */
(function(global){
  'use strict';

  const CONFIG = Object.freeze({
    artwork: 'assets/infinity-capital-note-master.webp',
    aspectRatio: 1776/831,
    serialPrefix: 'IC',
    // Coordinates are percentages of the approved front artwork.
    // They cover the placeholder serials printed into the approved master.
    serialZones: [
      {left:14.6, top:67.0, width:25.0, height:8.0, align:'left'},
      {left:64.7, top:27.2, width:25.0, height:8.0, align:'left'}
    ]
  });

  function normalizeHash(value){
    return String(value || '').toLowerCase().replace(/[^0-9a-f]/g,'');
  }

  function serialFromHash(hash){
    const h = normalizeHash(hash).padEnd(24,'0');
    return `${CONFIG.serialPrefix}-${h.slice(0,4).toUpperCase()}-${h.slice(4,8).toUpperCase()}-${h.slice(8,12).toUpperCase()}-${h.slice(12,16).toUpperCase()}`;
  }

  function makeFace(container, token){
    if(!container) throw new Error('note container required');
    const fullHash = normalizeHash(token && (token.commitHash || token.tokenHash || token.id));
    const serial = token && token.serial ? token.serial : serialFromHash(fullHash);
    container.innerHTML = '';
    container.classList.add('ic-note-face-v2');
    container.style.cssText += ';position:relative;overflow:hidden;aspect-ratio:'+CONFIG.aspectRatio+';background:#eee7d0;';

    const img = document.createElement('img');
    img.src = CONFIG.artwork;
    img.alt = 'Infinity Capital Bank of the NWO Reserve one Infinity note';
    img.style.cssText = 'display:block;width:100%;height:100%;object-fit:contain;';
    container.appendChild(img);

    CONFIG.serialZones.forEach((zone,index)=>{
      const el = document.createElement('div');
      el.className = 'ic-live-serial';
      el.dataset.serialZone = String(index+1);
      el.textContent = serial;
      el.title = fullHash ? 'Full Commit Token: '+fullHash : 'Pending Commit Token binding';
      el.style.cssText = [
        'position:absolute',`left:${zone.left}%`,`top:${zone.top}%`,`width:${zone.width}%`,`height:${zone.height}%`,
        'display:flex','align-items:center',zone.align==='right'?'justify-content:flex-end':'justify-content:flex-start',
        'padding:0 .45em','background:#eee7d0','color:#176239','font:700 clamp(8px,1.45vw,25px) ui-monospace,monospace',
        'letter-spacing:.055em','white-space:nowrap','overflow:hidden'
      ].join(';');
      container.appendChild(el);
    });

    container.dataset.fullTokenHash = fullHash;
    container.dataset.displaySerial = serial;
    return {serial, fullHash};
  }

  async function provisionalHash(payload){
    const body = JSON.stringify(payload || {}) + '|' + Date.now() + '|' + crypto.getRandomValues(new Uint32Array(4)).join('-');
    const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(body));
    return Array.from(new Uint8Array(digest),b=>b.toString(16).padStart(2,'0')).join('');
  }

  global.InfinityCapitalNote = Object.freeze({CONFIG, normalizeHash, serialFromHash, provisionalHash, makeFace});
})(window);
