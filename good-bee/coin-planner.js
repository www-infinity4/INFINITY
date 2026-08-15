const DATA_URL = './data/coin-planner.json'

const state = { data: null }

const els = {
  menuButton: document.querySelector('#menuButton'),
  mainNav: document.querySelector('#mainNav'),
  sourceGrid: document.querySelector('#sourceGrid'),
  stageGrid: document.querySelector('#stageGrid'),
  offerGrid: document.querySelector('#offerGrid'),
  form: document.querySelector('#optimizerForm'),
  retailBenchmark: document.querySelector('#retailBenchmark'),
  contractCost: document.querySelector('#contractCost'),
  userUnits: document.querySelector('#userUnits'),
  unitSettlement: document.querySelector('#unitSettlement'),
  sponsorFunding: document.querySelector('#sponsorFunding'),
  programFunding: document.querySelector('#programFunding'),
  infinityFunding: document.querySelector('#infinityFunding'),
  fundingStatus: document.querySelector('#fundingStatus'),
  fundingRows: document.querySelector('#fundingRows'),
  fundingMeter: document.querySelector('#fundingMeter span'),
  fundingExplanation: document.querySelector('#fundingExplanation'),
  year: document.querySelector('#year')
}

function escapeHtml(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;')
}

function numberValue(input) {
  const value = Number(input.value)
  return Number.isFinite(value) && value >= 0 ? value : 0
}

function money(value) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 2 }).format(value)
}

async function fetchData() {
  const response = await fetch(DATA_URL, { headers: { Accept: 'application/json' } })
  if (!response.ok) throw new Error(`Coin Planner data unavailable (${response.status})`)
  return response.json()
}

function renderSources() {
  els.sourceGrid.innerHTML = state.data.registrySources.map(source => `
    <article class="source-card">
      <span class="trust">${escapeHtml(source.trust)}</span>
      <h3>${escapeHtml(source.name)}</h3>
      <p>${escapeHtml(source.role)}</p>
    </article>
  `).join('')
}

function renderStages() {
  els.stageGrid.innerHTML = state.data.packageStages.map((stage, index) => `
    <article class="stage-card">
      <span>${String(index + 1).padStart(2, '0')}</span>
      <h3>${escapeHtml(stage.name)}</h3>
      <p>${escapeHtml(stage.description)}</p>
    </article>
  `).join('')
}

function renderOffers() {
  els.offerGrid.innerHTML = state.data.sampleOffers.map(offer => {
    const savings = Math.max(0, offer.retailBenchmark - offer.contractCost)
    const percent = offer.retailBenchmark > 0 ? Math.round((savings / offer.retailBenchmark) * 100) : 0
    return `
      <article class="sample-offer">
        <span class="category">${escapeHtml(offer.category)}</span>
        <h3>${escapeHtml(offer.business)}</h3>
        <p>${escapeHtml(offer.quantity)} ${escapeHtml(offer.unit)} · ${escapeHtml(offer.reason)}</p>
        <div class="offer-math">
          <div><span>Retail benchmark</span><strong>${money(offer.retailBenchmark)}</strong></div>
          <div><span>Contract cost</span><strong>${money(offer.contractCost)}</strong></div>
          <div><span>Illustrative reduction</span><strong>${percent}%</strong></div>
          <div><span>Status</span><strong>${offer.verified ? 'Verified' : 'Prototype only'}</strong></div>
        </div>
      </article>
    `
  }).join('')
}

function calculateFunding(event) {
  event?.preventDefault()

  const retail = numberValue(els.retailBenchmark)
  const cost = numberValue(els.contractCost)
  const units = numberValue(els.userUnits)
  const settlement = numberValue(els.unitSettlement)
  const sponsor = numberValue(els.sponsorFunding)
  const program = numberValue(els.programFunding)
  const infinity = numberValue(els.infinityFunding)
  const userContribution = units * settlement
  const totalFunding = userContribution + sponsor + program + infinity
  const gap = Math.max(0, cost - totalFunding)
  const surplus = Math.max(0, totalFunding - cost)
  const fundedPercent = cost > 0 ? Math.min(100, (totalFunding / cost) * 100) : 100
  const retailReduction = retail > 0 ? Math.max(0, 100 - (cost / retail) * 100) : 0

  els.fundingStatus.textContent = gap <= 0 ? 'Package fully funded in this demonstration' : `Package still needs ${money(gap)}`
  els.fundingRows.innerHTML = `
    <div class="funding-row"><span>Published retail-equivalent benchmark</span><strong>${money(retail)}</strong></div>
    <div class="funding-row"><span>Direct contracted cost</span><strong>${money(cost)}</strong></div>
    <div class="funding-row"><span>Difference from benchmark</span><strong>${retailReduction.toFixed(1)}%</strong></div>
    <div class="funding-row"><span>User contribution</span><strong>${units} Infinity units × ${money(settlement)} = ${money(userContribution)}</strong></div>
    <div class="funding-row"><span>Sponsor or advertiser funding</span><strong>${money(sponsor)}</strong></div>
    <div class="funding-row"><span>Program or benefit funding</span><strong>${money(program)}</strong></div>
    <div class="funding-row"><span>Infinity pool funding</span><strong>${money(infinity)}</strong></div>
    <div class="funding-row ${gap > 0 ? 'gap' : 'good'}"><span>Unfunded gap</span><strong>${money(gap)}</strong></div>
    <div class="funding-row good"><span>Excess funding or reserve</span><strong>${money(surplus)}</strong></div>
  `
  els.fundingMeter.style.width = `${fundedPercent}%`

  if (gap > 0) {
    els.fundingExplanation.textContent = 'This package remains a planning draft. Coin Planner must negotiate a lower real cost or find additional disclosed funding before it can be offered.'
  } else {
    els.fundingExplanation.textContent = 'The demonstration closes the contracted cost. Production publication would still require verified provider contracts, live capacity, taxes, cancellations, accessibility, payment settlement, and signed funding commitments.'
  }
}

function bindEvents() {
  els.menuButton?.addEventListener('click', () => {
    const open = els.mainNav.classList.toggle('open')
    els.menuButton.setAttribute('aria-expanded', String(open))
  })

  els.mainNav?.addEventListener('click', event => {
    if (event.target.matches('a')) {
      els.mainNav.classList.remove('open')
      els.menuButton?.setAttribute('aria-expanded', 'false')
    }
  })

  els.form?.addEventListener('submit', calculateFunding)
  ;[
    els.retailBenchmark,
    els.contractCost,
    els.userUnits,
    els.unitSettlement,
    els.sponsorFunding,
    els.programFunding,
    els.infinityFunding
  ].forEach(input => input?.addEventListener('input', calculateFunding))
}

async function init() {
  els.year.textContent = new Date().getFullYear()
  bindEvents()
  calculateFunding()

  try {
    state.data = await fetchData()
    renderSources()
    renderStages()
    renderOffers()
  } catch (error) {
    els.sourceGrid.innerHTML = `<p role="alert">${escapeHtml(error.message)}</p>`
  }
}

init()
