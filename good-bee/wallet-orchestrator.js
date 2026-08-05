const els = {
  menuButton: document.querySelector('#menuButton'),
  mainNav: document.querySelector('#mainNav'),
  form: document.querySelector('#packageForm'),
  destinationType: document.querySelector('#destinationType'),
  tripLength: document.querySelector('#tripLength'),
  includeAccessibility: document.querySelector('#includeAccessibility'),
  includeNfc: document.querySelector('#includeNfc'),
  includeProducts: document.querySelector('#includeProducts'),
  packageTitle: document.querySelector('#packageTitle'),
  packageRows: document.querySelector('#packageRows'),
  packageExplanation: document.querySelector('#packageExplanation'),
  graphSection: document.querySelector('#graph'),
  year: document.querySelector('#year')
}

const destinationNames = {
  beach: 'beach',
  mountain: 'mountain',
  city: 'city',
  sailing: 'sailing'
}

function escapeHtml(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;')
}

function buildPackage(event) {
  event?.preventDefault()

  const destination = destinationNames[els.destinationType.value] || 'travel'
  const days = Number(els.tripLength.value) || 7
  const hotelNights = days
  const hotelUnits = hotelNights * 100
  const rows = [
    ['Destination package', `${days}-day ${destination} plan`],
    ['Hotel claims', `${hotelNights} nights / ${hotelUnits} example Infinity units`],
    ['Transportation', `${Math.max(2, Math.ceil(days / 3))} ride claims`],
    ['Meals', `${days * 2} meal claims`]
  ]

  if (els.includeAccessibility.checked) {
    rows.push(['Accessibility coordination', 'Room, transport, communication, activity, and support review'])
  }

  if (els.includeNfc.checked) {
    rows.push(['NFC baseline', '$0.50-equivalent participating scan discount'])
    rows.push(['In-person offers', 'Local merchant and immediate-fulfillment bonuses compared automatically'])
  }

  if (els.includeProducts.checked) {
    const products = destination === 'beach'
      ? 'sun protection, accessible beach equipment, hydration, luggage support'
      : destination === 'mountain'
        ? 'weather layer, hydration, altitude planning, trail or mobility equipment'
        : destination === 'sailing'
          ? 'weather gear, adaptive sailing review, hydration, communications'
          : 'transit pass, event access, luggage support, local essentials'
    rows.push(['Useful product claims', products])
  }

  els.packageTitle.textContent = `${days}-day ${destination} package`
  els.packageRows.innerHTML = rows.map(([label, value]) => `
    <div class="package-row"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>
  `).join('')
  els.packageExplanation.textContent = 'AI presents one package, but every hotel night, ride, meal, discount, product, provider, expiration, and receipt remains a separate typed claim underneath.'
}

function integrateCoinPlanner() {
  if (els.mainNav && !els.mainNav.querySelector('a[href="coin-planner.html"]')) {
    const link = document.createElement('a')
    link.href = 'coin-planner.html'
    link.textContent = 'Coin Planner'
    const clearingLink = els.mainNav.querySelector('a[href="reciprocal-clearing.html"]')
    els.mainNav.insertBefore(link, clearingLink || null)
  }

  if (!els.graphSection || document.querySelector('#coin-planner')) return

  const section = document.createElement('section')
  section.id = 'coin-planner'
  section.className = 'section products-section'
  section.innerHTML = `
    <div class="section-heading">
      <div><p class="eyebrow">Infinity Coin Planner</p><h2>Search globally, buy locally and in bulk, then close the package funding gap.</h2></div>
      <p>Coin Planner discovers businesses through permitted sources, verifies merchant control and live capacity, negotiates local contracts, forecasts destination demand, stages appropriate products, and combines the results into Store Card packages.</p>
    </div>
    <div class="package-builder">
      <div class="package-form">
        <strong>$1,000 benchmark → 100-unit target</strong>
        <p>The retail-equivalent benchmark does not pay the provider. The planner separately shows contracted cost, traveler units, sponsor funding, program funding, Infinity funding, and any remaining gap.</p>
        <a class="button primary" href="coin-planner.html">Open Coin Planner</a>
      </div>
      <div class="package-output">
        <p class="eyebrow">Planner chain</p>
        <h3>Discover → verify → negotiate → stage → package → fund → fulfill</h3>
        <div class="package-row"><span>Business coverage</span><strong>Multiple official, licensed, open, and merchant-direct sources</strong></div>
        <div class="package-row"><span>Source order</span><strong>Local destination businesses first</strong></div>
        <div class="package-row"><span>Publication rule</span><strong>No package while a funding gap remains</strong></div>
      </div>
    </div>
  `

  els.graphSection.before(section)
}

function bindNavigation() {
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
}

function init() {
  integrateCoinPlanner()
  bindNavigation()
  els.form?.addEventListener('submit', buildPackage)
  ;[els.destinationType, els.tripLength, els.includeAccessibility, els.includeNfc, els.includeProducts]
    .forEach(control => control?.addEventListener('change', buildPackage))
  els.year.textContent = new Date().getFullYear()
  buildPackage()
}

init()
